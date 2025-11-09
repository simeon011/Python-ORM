
class RechargeEnergyMixin:
    MAX_ENERGY = 100

    def recharge_energy(self, amount: int):
        new_energy = self.energy + amount

        if new_energy > self.MAX_ENERGY:
            new_energy = self.MAX_ENERGY

        self.energy = new_energy
        self.save()

