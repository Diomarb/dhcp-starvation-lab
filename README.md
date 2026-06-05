# dhcp-starvation-lab
Lab ataque DHCP Starvation

Eunice Y. Francisca Fleming 2024-1185

Enlace de video: https://youtu.be/3lEO4Otkob4

Enlace de Playlist: https://www.youtube.com/playlist?list=PLedgCpC2B7oUOUOG7D6VLYsRR7i7bySIM

**Matrícula:** 2024-1185

---

## Descripción

Script Python que realiza un ataque **DHCP Starvation**, enviando masivamente peticiones DHCP Discover con MACs falsas y aleatorias para agotar el pool de IPs del servidor DHCP legítimo. Los dispositivos reales quedan sin poder obtener dirección IP (Denegación de Servicio).

---

## Requisitos

| Requisito | Detalle |
|-----------|---------|
| Sistema Operativo | Linux (probado en Linux2024 / Debian) |
| Python | 3.x |
| Librería | Scapy (`pip3 install scapy`) |
| Privilegios | root (sudo) |
| Simulador | GNS3 con DHCP server en IOU1 |

---

## Instalación

```bash
pip3 install scapy
```

---

## Uso

```bash
sudo python3 dhcp_starvation.py [opciones]
```

### Parámetros

| Parámetro | Descripción | Ejemplo |
|-----------|-------------|---------|
| `-c` / `--count` | Número de peticiones (0=infinito) | `-c 250` |
| `-d` / `--delay` | Delay entre peticiones (seg) | `-d 0.05` |
| `-v` / `--verbose` | Mostrar cada petición | `--verbose` |

### Ejemplo

```bash
sudo python3 dhcp_starvation.py -c 250 -v
```

---

## Topología

```
```
<img width="581" height="388" alt="image" src="https://github.com/user-attachments/assets/fff03090-6cab-47cc-bfd7-cd12cdff907b" />

### Tabla de Direccionamiento

| Dispositivo | IP | Máscara | Rol |
|-------------|-----|---------|-----|
| IOU1 | 10.11.85.1 | /24 | Gateway / DHCP Server |
| Linux2024 | 10.11.85.30 | /24 | Atacante |
| PC1 / PC2 | DHCP | /24 | Víctimas |

---

## Verificación del Ataque

```bash
# En IOU1 — ver pool agotado
show ip dhcp binding
show ip dhcp pool

# En VPCS — debe fallar
ip dhcp
# Resultado esperado: Can't find dhcp server
```
<img width="625" height="1117" alt="image" src="https://github.com/user-attachments/assets/05aae0ad-cc46-42fd-974a-95724583c1d5" />

<img width="800" height="180" alt="image" src="https://github.com/user-attachments/assets/c7d6659e-187c-4eee-9927-bd82119c67d3" />

<img width="593" height="223" alt="image" src="https://github.com/user-attachments/assets/5caf66ab-da85-4543-8b22-c38590513816" />

---

## Contramedida

```bash
# En IOU2 — Rate limiting por puerto
conf t
ip dhcp snooping
ip dhcp snooping vlan 1
no ip dhcp snooping information option
interface Ethernet0/0
 ip dhcp snooping trust
interface Ethernet0/3
 ip dhcp snooping limit rate 10
end
wr

# Verificar
show ip dhcp snooping statistics
```
<img width="591" height="302" alt="image" src="https://github.com/user-attachments/assets/2929a0f8-8cd6-459b-a025-651123a8bc23" />

<img width="975" height="113" alt="image" src="https://github.com/user-attachments/assets/dce22f8f-c938-4e1b-8eb9-bd0da2f9031a" />

Las PC vuelven a obtener IP via DHCP

<img width="556" height="138" alt="image" src="https://github.com/user-attachments/assets/205119f7-bd7b-4304-9b6b-2aa324be5053" />


---

## Video

> Enlace al video de demostración: https://youtu.be/3lEO4Otkob4

---

## Documentación

Ver archivo incluido en este repositorio.
