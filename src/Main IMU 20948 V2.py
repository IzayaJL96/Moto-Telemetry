import machine
import time

i2c0 = machine.I2C(0, scl=machine.Pin(22), sda=machine.Pin(21), freq=400000)
i2c1 = machine.I2C(1, scl=machine.Pin(4),  sda=machine.Pin(5),  freq=400000)

ICM_ADDR = 0x69

def set_bank(i2c, bank):
    i2c.writeto_mem(ICM_ADDR, 0x7F, bytes([bank & 0x03]))
    time.sleep_ms(5)

def who_am_i(i2c):
    set_bank(i2c, 0)
    return i2c.readfrom_mem(ICM_ADDR, 0x00, 1)[0]

def init_icm(i2c):
    set_bank(i2c, 0)
    i2c.writeto_mem(ICM_ADDR, 0x06, bytes([0x80]))  # Reset
    time.sleep_ms(100)
    i2c.writeto_mem(ICM_ADDR, 0x06, bytes([0x01]))  # Despertar
    time.sleep_ms(50)
    i2c.writeto_mem(ICM_ADDR, 0x07, bytes([0x00]))  # Accel + gyro ON
    time.sleep_ms(50)
    set_bank(i2c, 2)
    i2c.writeto_mem(ICM_ADDR, 0x14, bytes([0x01]))  # Accel ±2g
    i2c.writeto_mem(ICM_ADDR, 0x01, bytes([0x01]))  # Gyro ±250°/s
    time.sleep_ms(50)
    set_bank(i2c, 0)

def read_icm(i2c):
    set_bank(i2c, 0)
    a = i2c.readfrom_mem(ICM_ADDR, 0x2D, 6)
    g = i2c.readfrom_mem(ICM_ADDR, 0x33, 6)

    def s(v): return v - 65536 if v > 32767 else v

    return (
        s(a[0] << 8 | a[1]) / 16384.0,
        s(a[2] << 8 | a[3]) / 16384.0,
        s(a[4] << 8 | a[5]) / 16384.0,
        s(g[0] << 8 | g[1]) / 131.0,
        s(g[2] << 8 | g[3]) / 131.0,
        s(g[4] << 8 | g[5]) / 131.0,
    )

def intentar_reiniciar(i2c, nombre):
    """Intenta reconectar un sensor caído — retorna True si lo logra"""
    try:
        chip_id = who_am_i(i2c)
        if chip_id == 0xEA:
            init_icm(i2c)
            print(f"  ↺ {nombre} reconectado OK")
            return True
    except OSError:
        pass
    return False

# ── Configuración ──────────────────────────────────────────────
SENSORES = [
    {"i2c": i2c0, "nombre": "SENSOR_1_PECHO",  "activo": False, "errores": 0},
    {"i2c": i2c1, "nombre": "SENSOR_2_HOMBRO", "activo": False, "errores": 0},
]

# ── Inicialización ─────────────────────────────────────────────
print("=== Inicializando sensores ===\n")

for s in SENSORES:
    try:
        chip_id = who_am_i(s["i2c"])
        if chip_id == 0xEA:
            init_icm(s["i2c"])
            s["activo"] = True
            print(f"✓ {s['nombre']} OK")
        else:
            print(f"✗ {s['nombre']} WHO_AM_I: 0x{chip_id:02X} (esperado 0xEA)")
    except OSError as e:
        print(f"✗ {s['nombre']} no responde: {e}")

activos = sum(1 for s in SENSORES if s["activo"])
print(f"\n{activos} sensor(es) activo(s). Iniciando lectura...\n")

# ── Loop de lectura ────────────────────────────────────────────
REINTENTOS_MAX = 3   # intentos antes de marcar como perdido
PAUSA_MS       = 500

muestra = 0
while True:
    muestra += 1
    hay_datos = False

    for s in SENSORES:
        if not s["activo"]:
            # Intentar reconectar cada 5 muestras
            if muestra % 5 == 0:
                print(f"  ? Intentando reconectar {s['nombre']}...")
                s["activo"] = intentar_reiniciar(s["i2c"], s["nombre"])
            continue

        try:
            ax, ay, az, gx, gy, gz = read_icm(s["i2c"])
            s["errores"] = 0  # reset contador de errores consecutivos
            hay_datos = True
            print(f"[{muestra:3d}] {s['nombre']:20s} | "
                  f"Accel(g) {ax:6.3f} {ay:6.3f} {az:6.3f} | "
                  f"Gyro(°/s) {gx:7.2f} {gy:7.2f} {gz:7.2f}")

        except OSError as e:
            s["errores"] += 1
            print(f"  ! {s['nombre']} error #{s['errores']}: {e}")

            if s["errores"] >= REINTENTOS_MAX:
                print(f"  ✗ {s['nombre']} marcado como INACTIVO — reconexión automática cada 5 muestras")
                s["activo"] = False
                s["errores"] = 0
            else:
                # Reintento inmediato
                print(f"    Reintentando...")
                s["activo"] = intentar_reiniciar(s["i2c"], s["nombre"])

    if hay_datos:
        print("─" * 75)

    time.sleep_ms(PAUSA_MS)