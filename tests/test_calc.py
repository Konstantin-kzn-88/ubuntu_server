from unittest import TestCase, main
from calc import calc_strait_fire, calc_probit, calc_sp_explosion


class ServerTest(TestCase):

    # START 1. Тестирование пожара пролива (strait_fire)
    def test_strait_fire_liguid(self):
        self.assertEqual(
            round(calc_strait_fire.Strait_fire().termal_radiation_point(S_spill=918, m_sg=0.06, mol_mass=95,
                                                                        t_boiling=68, wind_velocity=2, radius=40), 1),
            6.3)

    def test_strait_fire_greater_than_zero(self):
        self.assertGreater(
            round(calc_strait_fire.Strait_fire().termal_radiation_point(S_spill=918, m_sg=0.06, mol_mass=95,
                                                                        t_boiling=68, wind_velocity=2, radius=40), 1),
            0)

    def test_strait_fire_lpg(self):
        self.assertEqual(
            round(calc_strait_fire.Strait_fire().termal_radiation_point(S_spill=20, m_sg=0.1, mol_mass=44,
                                                                        t_boiling=-15, wind_velocity=1, radius=50), 1),
            0.8)

    def test_strait_fire_with_null_param(self):
        with self.assertRaises(ValueError) as e:
            calc_strait_fire.Strait_fire().termal_radiation_point(S_spill=0, m_sg=0.1, mol_mass=44,
                                                                  t_boiling=0, wind_velocity=1, radius=50)

        self.assertEqual('Фукнция не может принимать нулевые параметры', e.exception.args[0])

        with self.assertRaises(ValueError) as e:
            calc_strait_fire.Strait_fire().termal_radiation_point(S_spill=20, m_sg=0, mol_mass=0,
                                                                  t_boiling=200, wind_velocity=0, radius=50)

        self.assertEqual('Фукнция не может принимать нулевые параметры', e.exception.args[0])

    def test_count_array_result(self):
        for s in range(20, 200, 25):
            self.assertEqual(len(calc_strait_fire.Strait_fire().termal_radiation_array(S_spill=s, m_sg=0.1, mol_mass=44,
                                                                                       t_boiling=-15, wind_velocity=1)[0]),
                             len(calc_strait_fire.Strait_fire().termal_radiation_array(S_spill=s, m_sg=0.1, mol_mass=44,
                                                                                       t_boiling=-15, wind_velocity=1)[1]))

            self.assertEqual(len(calc_strait_fire.Strait_fire().termal_radiation_array(S_spill=s, m_sg=0.3, mol_mass=144,
                                                                                       t_boiling=-10, wind_velocity=1)[2]),
                             len(calc_strait_fire.Strait_fire().termal_radiation_array(S_spill=s, m_sg=0.3, mol_mass=144,
                                                                                       t_boiling=-10, wind_velocity=1)[3]))
        # END

    # START 2. Тестирование пробит-функции

    def test_probit_check(self):
        self.assertEqual(calc_probit.Probit().probit_check(probit=11), 8.09)
        self.assertEqual(calc_probit.Probit().probit_check(probit=2), 0)
        self.assertEqual(calc_probit.Probit().probit_check(probit=3.33), 3.33)

    def test_probability(self):
        self.assertEqual(calc_probit.Probit().probability(probit=8.99), 0.99)
        self.assertEqual(calc_probit.Probit().probability(probit=-12), 0)
        self.assertEqual(round(calc_probit.Probit().probability(probit=3.35), 2), 0.05)

    def test_probit_explosion_with_null_param(self):
        with self.assertRaises(ValueError) as e:
            calc_probit.Probit().probit_explosion(delta_P=0, impuls=161)
        self.assertEqual('Фукнция не может принимать нулевые параметры', e.exception.args[0])

        with self.assertRaises(ValueError) as e:
            calc_probit.Probit().probit_explosion(delta_P=0, impuls=0)
        self.assertEqual('Фукнция не может принимать нулевые параметры', e.exception.args[0])

    def test_probit_fireball_with_null_param(self):
        with self.assertRaises(ValueError) as e:
            calc_probit.Probit().probit_fireball(time=0, q_ball=125)
        self.assertEqual('Фукнция не может принимать нулевые параметры', e.exception.args[0])

        with self.assertRaises(ValueError) as e:
            calc_probit.Probit().probit_fireball(time=0, q_ball=0)
        self.assertEqual('Фукнция не может принимать нулевые параметры', e.exception.args[0])

    def test_probit_strait_fire_with_null_param(self):
        with self.assertRaises(ValueError) as e:
            calc_probit.Probit().probit_strait_fire(dist=0, q_max=0)
        self.assertEqual('math domain error', e.exception.args[0])

        with self.assertRaises(ValueError) as e:
            calc_probit.Probit().probit_strait_fire(dist=10, q_max=0)
        self.assertEqual('math domain error', e.exception.args[0])

    # END

    # START 3. Тестирование взрыва (СП 12.13130-2009)
    def test_explosion_point(self):
        self.assertEqual(
            round(
                calc_sp_explosion.Explosion().explosion_point(mass=254400, heat_of_combustion=46000, z=0.1, radius=500)[
                    0], 2), 15.5)

    def test_explosion_point_greater_than_zero(self):
        for m in range(100, 1000, 250):
            self.assertGreater(
                round(
                    calc_sp_explosion.Explosion().explosion_point(mass=m, heat_of_combustion=101000, z=0.1,
                                                                  radius=50)[0], 1), 0)

    def test_explosion_with_null_param(self):
        with self.assertRaises(ValueError) as e:
            calc_sp_explosion.Explosion().explosion_point(mass=0, heat_of_combustion=101000, z=0.1, radius=50)
        self.assertEqual('Фукнция не может принимать нулевые параметры', e.exception.args[0])

        with self.assertRaises(ValueError) as e:
            calc_sp_explosion.Explosion().explosion_point(mass=0, heat_of_combustion=0, z=0.1, radius=0)
        self.assertEqual('Фукнция не может принимать нулевые параметры', e.exception.args[0])

    def test_count_array_result_explosion(self):
        for m in range(100, 1000, 250):
            self.assertEqual(
                len(calc_sp_explosion.Explosion().explosion_array(mass=m, heat_of_combustion=46000, z=0.1)[0]),
                len(calc_sp_explosion.Explosion().explosion_array(mass=m, heat_of_combustion=46000, z=0.1)[1]))

            self.assertEqual(
                len(calc_sp_explosion.Explosion().explosion_array(mass=m, heat_of_combustion=46000, z=0.1)[2]),
                len(calc_sp_explosion.Explosion().explosion_array(mass=m, heat_of_combustion=46000, z=0.1)[3]))
        # END


if __name__ == '__main__':
    main()
