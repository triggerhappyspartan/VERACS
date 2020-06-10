import os
import sys
from simulate_exchanger import h5_converter

if __name__ == "__main__":
    dir_list = ['child_75_1','child_75_3','child_75_32','child_75_40','child_75_51','child_76_15','child_76_18','child_76_26','child_76_3','child_76_34','child_76_40',
                'child_77_14','child_77_27','child_77_36','child_77_51','child_77_56','child_77_57','child_77_59','child_78_0','child_78_1','child_78_11','child_78_13',
                'child_78_14','child_78_19','child_78_22','child_78_28','child_78_35','child_78_46','child_78_49','child_78_5','child_78_53','child_78_56','child_78_59',
                'child_78_8','child_79_0','child_79_10','child_79_11','child_79_12','child_79_14','child_79_15','child_79_16','child_79_17','child_79_18','child_79_22',
                'child_79_23','child_79_24','child_79_25','child_79_27','child_79_28','child_79_29','child_79_31','child_79_34','child_79_35','child_79_36','child_79_38',
                'child_79_39','child_79_40','child_79_41','child_79_42','child_79_45','child_79_46','child_79_47','child_79_48','child_79_49','child_79_50','child_79_51',
                'child_79_52','child_79_53','child_79_54','child_79_55','child_79_56','child_79_57','child_79_58','child_79_59','child_79_60','child_79_61','child_79_62',
                'child_79_63','child_79_64','child_79_65','child_79_66','child_79_67','child_79_68','child_79_69','child_79_7','child_79_70','child_79_71','child_79_72',
                'child_79_73','child_79_74','child_79_75','child_79_76','child_79_77','child_79_78','child_79_79','child_79_9','child_80_31','child_80_33','child_82_15',
                'child_87_53','child_88_19','child_90_38','child_91_11','child_92_21','child_92_24','child_92_36','child_92_7','child_94_31','child_94_44','child_94_8',
                'child_95_26','child_95_38','child_95_45','child_95_5','child_96_10','child_97_24','child_97_31','child_97_33','child_97_35','child_97_42','child_97_43',
                'child_97_55','child_97_56','child_97_59','child_98_14','child_98_17','child_98_33','child_98_39','child_98_4','child_98_41','child_98_5','child_98_51',
                'child_98_58','child_98_7','child_98_8','child_98_9','child_99_1','child_99_17','child_99_21','child_99_36','child_99_4','child_99_42','child_99_43',
                'child_99_45','child_99_47','child_99_48','child_99_49','child_99_51','child_99_53','child_99_54','child_99_56','child_99_57','child_99_58','child_99_59']


    for foo in dir_list:
        command = f'cd Simulate_Files/{foo} & python ../../simulate_exchanger.py --file {foo}_sim.out'
        os.system(command)