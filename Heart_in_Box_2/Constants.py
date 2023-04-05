
'''--- NiMotion BLM Registers ---'''

# Input Registers <Read-only registers>
MCU_ID          = 209       # 0x00D1 
STATUS_WORD     = 897       # 0x0381
ACTUAL_SPEED    = 981       # 0x03D5
BUS_VOLTAGE     = 503       # 0x01F7
TEMPERATURE     = 504       # 0x01F8
RATED_CURRENT   = 101       # 0x0065
ACTUAL_CURRENT  = 996       # 0x03E4


# Holding Register <Read/Write registers>
SERVO_ID        = 560       # 0x0230
BAUDRATE        = 561       # 0x0231
CONTROL_WORD    = 896       # 0x0380
MODE_OPER       = 962       # 0x03C2
MAX_TORQUE      = 988       # 0x03DC 
MAX_SPEED       = 1014      # 0x03F6
ACC_CURVE       = 1026      # 0x0402
TARGET_SPEED    = 1096      # 0x0448


# Control Word Commands
STOP            = 6         # 0x06
SWITCH_ON       = 7         # 0x07
DRIVE           = 15        # 0x0F


# Dictionaries
OPMODE_DICT = { '0x202': "Velocity Mode",
                '0x02' : "Velocity Mode",
                '0x303': "Profile Velocity Mode",
                '0x03' :  "Profile Velocity Mode"}

STATUS_DICT ={ '0x1260': 'Switch on disabled',
               '0x1221': 'Ready to switch on',
               '0x03'  : 'Switched on',
               '0x1233': 'Switched on',
               '0x1237': 'Pausing, target speed not reached',
               '0x221' : 'still unknown',
               '0x237' : 'Running, target speed not reached',
               '0x1637': 'Operation enabled',
               '0x637' : 'Running, target speed reached',
               '0xa37' : 'Quick Stop active',
               '0x1a37' : 'Quick Stop active',
               '0xe37' : 'still unknown',}

ACC_CURVE_DICT = {  '0x00': 'Trepzoid',
                    '0x03': 'S-curve'}

BAUD_RATE_DICT = { 0: 1200,  1: 2400,   2: 4800,   3: 9600,   4: 19200,    5: 38400,
                   6: 57600, 7: 115200, 8: 256000, 9: 500000, 10: 1000000, 11: 1500000 }

