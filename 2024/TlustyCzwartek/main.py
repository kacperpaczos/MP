def procent_paczkow(masa_przed_tlustym_czwartkiem):
    masa_po_tlustym_czwartku = 100
    przybylo_masy = masa_po_tlustym_czwartku - masa_przed_tlustym_czwartkiem
    procent_masy_paczkow = (przybylo_masy / masa_po_tlustym_czwartku) * 100
    return procent_masy_paczkow

masa_przed_tlustym_czwartkiem = int(input())
if 40 <= masa_przed_tlustym_czwartkiem <= 100:
    print(f"{procent_paczkow(masa_przed_tlustym_czwartkiem):.0f}")
