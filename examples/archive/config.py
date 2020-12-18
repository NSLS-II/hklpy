''' '''

import sys
import logging


LOG_FORMAT = "%(asctime)-15s [%(name)5s:%(levelname)s] %(message)s"
EXAMPLE_LOGGER = 'ophyd_examples'


def setup_loggers(logger_names, fmt=LOG_FORMAT):
    fmt = logging.Formatter(LOG_FORMAT)
    for name in logger_names:
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(fmt)
        logger.addHandler(handler)


setup_loggers((EXAMPLE_LOGGER, ))
logger = logging.getLogger(EXAMPLE_LOGGER)


motor_recs = ['XF:31IDA-OP{Tbl-Ax:X1}Mtr',
              'XF:31IDA-OP{Tbl-Ax:X2}Mtr',
              'XF:31IDA-OP{Tbl-Ax:X3}Mtr',
              'XF:31IDA-OP{Tbl-Ax:X4}Mtr',
              'XF:31IDA-OP{Tbl-Ax:X5}Mtr',
              'XF:31IDA-OP{Tbl-Ax:X6}Mtr',
              ]

fake_motors = [{'readback': 'XF:31IDA-OP{Tbl-Ax:FakeMtr}-I',
                'setpoint': 'XF:31IDA-OP{Tbl-Ax:FakeMtr}-SP',
                'moving': 'XF:31IDA-OP{Tbl-Ax:FakeMtr}Sts:Moving-Sts',
                'actuate': 'XF:31IDA-OP{Tbl-Ax:FakeMtr}Cmd:Go-Cmd.PROC',
                'stop': 'XF:31IDA-OP{Tbl-Ax:FakeMtr}Cmd:Stop-Cmd.PROC',
                },

               ]

fake_sensors = ['XF:31IDA-BI{Dev:1}E-I',
                'XF:31IDA-BI{Dev:2}E-I',
                'XF:31IDA-BI{Dev:3}E-I',
                'XF:31IDA-BI{Dev:4}E-I',
                'XF:31IDA-BI{Dev:5}E-I',
                'XF:31IDA-BI{Dev:6}E-I',
                ]

ad_plugins = {'image': ['image1:', ],
              'roi': ['ROI1:', 'ROI2:', 'ROI3:', 'ROI4:'],
              'file': ['netCDF1:', 'TIFF1:', 'JPEG1:', 'Nexus1:', 'HDF1:', 'Magick1:', ],
              'proc': ['Proc1:', ],
              'stats': ['Stats1:', 'Stats2:', 'Stats3:', 'Stats4:', 'Stats5:', ],
              'overlay': [('Over1:', 1, 8), ],
              'trans': ['Trans1:', ],
              'cc': ['CC1:', 'CC2:', ],
              }

sim_areadetector = [{'prefix': 'XF:31IDA-BI{Cam:Tbl}',
                     'cam': 'cam1:',
                     },
                    {'prefix': 'XF:31IDA-BI{Cam:Tbl}',
                     'cam': 'cam2:',
                     }
                    ]

# PV names for the channel access server to create
server_pvnames = ['_server_pv_',
                  ]

# this is a real instrument - it is not currently used, but be cautious!
scalers = ['XF:23ID2-ES{Sclr:1}']
