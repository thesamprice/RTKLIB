import ctypes
import warnings
#pip install enum34
import enum

my_endian=ctypes.Structure

lib_file = "rtklib.dylib"
rtklib = ctypes.CDLL(lib_file)

class NAVIGATION_SYSTEM(enum.Enum):
    SYS_NONE = 0
    SYS_GPS  = 1
    SYS_SBS  = 2
    SYS_GLO  = 4
    SYS_GAL  = 8
    SYS_QZS  = 16
    SYS_CMP  = 32
    SYS_LEO  = 64
    SYS_ALL  = 255

class TIME_SYSTEM(enum.Enum):
    TSYS_GPS = 0
    TSYS_UTC = 1
    TSYS_GLO = 2
    TSYS_GAL = 3
    TSYS_QZS = 4
    TSYS_CMP = 5

class TIME_SYSTEM2(enum.Enum):
    TIMES_GPST = 0
    TIMES_UTC  = 1
    TIMES_JST  = 2

class OBSERVATION_CODE(enum.Enum):
    CODE_NONE = 0
    CODE_L1C  = 1
    CODE_L1P  = 2
    CODE_L1W  = 3
    CODE_L1Y  = 4
    CODE_L1M  = 5
    CODE_L1N  = 6
    CODE_L1S  = 7
    CODE_L1L  = 8
    CODE_L1E  = 9
    CODE_L1A  = 10
    CODE_L1B  = 11
    CODE_L1X  = 12
    CODE_L1Z  = 13
    CODE_L2C  = 14
    CODE_L2D  = 15
    CODE_L2S  = 16
    CODE_L2L  = 17
    CODE_L2X  = 18
    CODE_L2P  = 19
    CODE_L2W  = 20
    CODE_L2Y  = 21
    CODE_L2M  = 22
    CODE_L2N  = 23
    CODE_L5I  = 24
    CODE_L5Q  = 25
    CODE_L5X  = 26
    CODE_L7I  = 27
    CODE_L7Q  = 28
    CODE_L7X  = 29
    CODE_L6A  = 30
    CODE_L6B  = 31
    CODE_L6C  = 32
    CODE_L6X  = 33
    CODE_L6Z  = 34
    CODE_L6S  = 35
    CODE_L6L  = 36
    CODE_L8I  = 37
    CODE_L8Q  = 38
    CODE_L8X  = 39
    CODE_L2I  = 40
    CODE_L2Q  = 41
    CODE_L6I  = 42
    CODE_L6Q  = 43
    CODE_L3I  = 44
    CODE_L3Q  = 45
    CODE_L3X  = 46
    CODE_L1I  = 47
    CODE_L1Q  = 48
    MAXCODE   = 48

class POSITIONING_MODE(enum.Enum):
    PMODE_SINGLE     = 0
    PMODE_DGPS       = 1
    PMODE_KINEMA     = 2
    PMODE_STATIC     = 3
    PMODE_MOVEB      = 4
    PMODE_FIXED      = 5
    PMODE_PPP_KINEMA = 6
    PMODE_PPP_STATIC = 7
    PMODE_PPP_FIXED  = 8

class SOLUTION_FORMAT(enum.Enum):
    SOLF_LLH  = 0
    SOLF_XYZ  = 1
    SOLF_ENU  = 2
    SOLF_NMEA = 3
    SOLF_GSIF = 4

class SOLUTION_STATUS(enum.Enum):
    SOLQ_NONE   = 0
    SOLQ_FIX    = 1
    SOLQ_FLOAT  = 2
    SOLQ_SBAS   = 3
    SOLQ_DGPS   = 4
    SOLQ_SINGLE = 5
    SOLQ_PPP    = 6
    SOLQ_DR     = 7

class IONOSPHERE_OPTIONS(enum.Enum):
    IONOOPT_OFF  = 0
    IONOOPT_BRDC = 1
    IONOOPT_SBAS = 2
    IONOOPT_IFLC = 3
    IONOOPT_EST  = 4
    IONOOPT_TEC  = 5
    IONOOPT_QZS  = 6
    IONOOPT_LEX  = 7
    IONOOPT_STEC = 8




class gtime_t (my_endian):
    """
gtime_t{        /* time struct */
    time_t time;        /* time (s) expressed by standard time_t */
    double sec;         /* fraction of second under 1 s */
} """
    _pack_ = 1

    _fields_ = [ ("time" , ctypes.c_int64 ),
                 ("sec"  , ctypes.c_double )]
    def SetConstants(self):
        pass


class obsd_t (my_endian):
    """
obsd_t{        /* observation data record */
    gtime_t time;       /* receiver sampling time (GPST) */
    unsigned char sat,rcv; /* satellite/receiver number */
    unsigned char SNR [NFREQ+NEXOBS]; /* signal strength (0.25 dBHz) */
    unsigned char LLI [NFREQ+NEXOBS]; /* loss of lock indicator */
    unsigned char code[NFREQ+NEXOBS]; /* code indicator (CODE_???) */
    double L[NFREQ+NEXOBS]; /* observation data carrier-phase (cycle) */
    double P[NFREQ+NEXOBS]; /* observation data pseudorange (m) */
    float  D[NFREQ+NEXOBS]; /* observation data doppler frequency (Hz) */
} """
    _pack_ = 1

    _fields_ = [ ("time"       , gtime_t ),
                 ("sat"        , ctypes.c_ubyte ),
                 ("rcv"        , ctypes.c_ubyte ),
                 ("SNR"        , ctypes.c_ubyte  * 3 ),
                 ("LLI"        , ctypes.c_ubyte  * 3 ),
                 ("code"       , ctypes.c_ubyte  * 3 ),
                 ("pad_216_40" , ctypes.c_ubyte  * 5 ),
                 ("L"          , ctypes.c_double * 3 ),
                 ("P"          , ctypes.c_double * 3 ),
                 ("D"          , ctypes.c_float  * 3 ),
                 ("pad_736_32" , ctypes.c_ubyte  * 4 )]
    def SetConstants(self):
        pass


class obs_t (my_endian):
    """
obs_t{        /* observation data */
    int n,nmax;         /* number of obervation data/allocated */
    obsd_t *data;       /* observation data records */
} """
    _pack_ = 1

    _fields_ = [ ("n"    , ctypes.c_int ),
                 ("nmax" , ctypes.c_int ),
                 ("data" , ctypes.POINTER(obsd_t) )]
    def SetConstants(self):
        pass


class erpd_t (my_endian):
    """
erpd_t{        /* earth rotation parameter data type */
    double mjd;         /* mjd (days) */
    double xp,yp;       /* pole offset (rad) */
    double xpr,ypr;     /* pole offset rate (rad/day) */
    double ut1_utc;     /* ut1-utc (s) */
    double lod;         /* length of day (s/day) */
} """
    _pack_ = 1

    _fields_ = [ ("mjd"     , ctypes.c_double ),
                 ("xp"      , ctypes.c_double ),
                 ("yp"      , ctypes.c_double ),
                 ("xpr"     , ctypes.c_double ),
                 ("ypr"     , ctypes.c_double ),
                 ("ut1_utc" , ctypes.c_double ),
                 ("lod"     , ctypes.c_double )]
    def SetConstants(self):
        pass


class erp_t (my_endian):
    """
erp_t{        /* earth rotation parameter type */
    int n,nmax;         /* number and max number of data */
    erpd_t *data;       /* earth rotation parameter data */
} """
    _pack_ = 1

    _fields_ = [ ("n"    , ctypes.c_int ),
                 ("nmax" , ctypes.c_int ),
                 ("data" , ctypes.POINTER(erpd_t) )]
    def SetConstants(self):
        pass


class pcv_t (my_endian):
    """
pcv_t{        /* antenna parameter type */
    int sat;            /* satellite number (0:receiver) */
    char type[MAXANT];  /* antenna type */
    char code[MAXANT];  /* serial number or satellite code */
    gtime_t ts,te;      /* valid time start and end */
    double off[NFREQ][ 3]; /* phase center offset e/n/u or x/y/z (m) */
    double var[NFREQ][19]; /* phase center variation (m) */
                        /* el=90,85,...,0 or nadir=0,1,2,3,... (deg) */
} """
    _pack_ = 1

    _fields_ = [ ("sat"         , ctypes.c_int ),
                 ("type"        , ctypes.c_char    * 64 ),
                 ("code"        , ctypes.c_char    * 64 ),
                 ("pad_1056_32" , ctypes.c_ubyte   * 4 ),
                 ("ts"          , gtime_t ),
                 ("te"          , gtime_t ),
                 ("off"         , (ctypes.c_double * 3) * 3 ),
                 ("var"         , (ctypes.c_double * 19) * 3 )]
    def SetConstants(self):
        pass


class pcvs_t (my_endian):
    """
pcvs_t{        /* antenna parameters type */
    int n,nmax;         /* number of data/allocated */
    pcv_t *pcv;         /* antenna parameters data */
} """
    _pack_ = 1

    _fields_ = [ ("n"    , ctypes.c_int ),
                 ("nmax" , ctypes.c_int ),
                 ("pcv"  , ctypes.POINTER(pcv_t) )]
    def SetConstants(self):
        pass


class alm_t (my_endian):
    """
alm_t{        /* almanac type */
    int sat;            /* satellite number */
    int svh;            /* sv health (0:ok) */
    int svconf;         /* as and sv config */
    int week;           /* GPS/QZS: gps week, GAL: galileo week */
    gtime_t toa;        /* Toa */
                        /* SV orbit parameters */
    double A,e,i0,OMG0,omg,M0,OMGd;
    double toas;        /* Toa (s) in week */
    double f0,f1;       /* SV clock parameters (af0,af1) */
} """
    _pack_ = 1

    _fields_ = [ ("sat"    , ctypes.c_int ),
                 ("svh"    , ctypes.c_int ),
                 ("svconf" , ctypes.c_int ),
                 ("week"   , ctypes.c_int ),
                 ("toa"    , gtime_t ),
                 ("A"      , ctypes.c_double ),
                 ("e"      , ctypes.c_double ),
                 ("i0"     , ctypes.c_double ),
                 ("OMG0"   , ctypes.c_double ),
                 ("omg"    , ctypes.c_double ),
                 ("M0"     , ctypes.c_double ),
                 ("OMGd"   , ctypes.c_double ),
                 ("toas"   , ctypes.c_double ),
                 ("f0"     , ctypes.c_double ),
                 ("f1"     , ctypes.c_double )]
    def SetConstants(self):
        pass


class eph_t (my_endian):
    """
eph_t{        /* GPS/QZS/GAL broadcast ephemeris type */
    int sat;            /* satellite number */
    int iode,iodc;      /* IODE,IODC */
    int sva;            /* SV accuracy (URA index) */
    int svh;            /* SV health (0:ok) */
    int week;           /* GPS/QZS: gps week, GAL: galileo week */
    int code;           /* GPS/QZS: code on L2, GAL/CMP: data sources */
    int flag;           /* GPS/QZS: L2 P data flag, CMP: nav type */
    gtime_t toe,toc,ttr; /* Toe,Toc,T_trans */
                        /* SV orbit parameters */
    double A,e,i0,OMG0,omg,M0,deln,OMGd,idot;
    double crc,crs,cuc,cus,cic,cis;
    double toes;        /* Toe (s) in week */
    double fit;         /* fit interval (h) */
    double f0,f1,f2;    /* SV clock parameters (af0,af1,af2) */
    double tgd[4];      /* group delay parameters */
                        /* GPS/QZS:tgd[0]=TGD */
                        /* GAL    :tgd[0]=BGD E5a/E1,tgd[1]=BGD E5b/E1 */
                        /* CMP    :tgd[0]=BGD1,tgd[1]=BGD2 */
} """
    _pack_ = 1

    _fields_ = [ ("sat"  , ctypes.c_int ),
                 ("iode" , ctypes.c_int ),
                 ("iodc" , ctypes.c_int ),
                 ("sva"  , ctypes.c_int ),
                 ("svh"  , ctypes.c_int ),
                 ("week" , ctypes.c_int ),
                 ("code" , ctypes.c_int ),
                 ("flag" , ctypes.c_int ),
                 ("toe"  , gtime_t ),
                 ("toc"  , gtime_t ),
                 ("ttr"  , gtime_t ),
                 ("A"    , ctypes.c_double ),
                 ("e"    , ctypes.c_double ),
                 ("i0"   , ctypes.c_double ),
                 ("OMG0" , ctypes.c_double ),
                 ("omg"  , ctypes.c_double ),
                 ("M0"   , ctypes.c_double ),
                 ("deln" , ctypes.c_double ),
                 ("OMGd" , ctypes.c_double ),
                 ("idot" , ctypes.c_double ),
                 ("crc"  , ctypes.c_double ),
                 ("crs"  , ctypes.c_double ),
                 ("cuc"  , ctypes.c_double ),
                 ("cus"  , ctypes.c_double ),
                 ("cic"  , ctypes.c_double ),
                 ("cis"  , ctypes.c_double ),
                 ("toes" , ctypes.c_double ),
                 ("fit"  , ctypes.c_double ),
                 ("f0"   , ctypes.c_double ),
                 ("f1"   , ctypes.c_double ),
                 ("f2"   , ctypes.c_double ),
                 ("tgd"  , ctypes.c_double * 4 )]
    def SetConstants(self):
        pass


class geph_t (my_endian):
    """
geph_t{        /* GLONASS broadcast ephemeris type */
    int sat;            /* satellite number */
    int iode;           /* IODE (0-6 bit of tb field) */
    int frq;            /* satellite frequency number */
    int svh,sva,age;    /* satellite health, accuracy, age of operation */
    gtime_t toe;        /* epoch of epherides (gpst) */
    gtime_t tof;        /* message frame time (gpst) */
    double pos[3];      /* satellite position (ecef) (m) */
    double vel[3];      /* satellite velocity (ecef) (m/s) */
    double acc[3];      /* satellite acceleration (ecef) (m/s^2) */
    double taun,gamn;   /* SV clock bias (s)/relative freq bias */
    double dtaun;       /* delay between L1 and L2 (s) */
} """
    _pack_ = 1

    _fields_ = [ ("sat"   , ctypes.c_int ),
                 ("iode"  , ctypes.c_int ),
                 ("frq"   , ctypes.c_int ),
                 ("svh"   , ctypes.c_int ),
                 ("sva"   , ctypes.c_int ),
                 ("age"   , ctypes.c_int ),
                 ("toe"   , gtime_t ),
                 ("tof"   , gtime_t ),
                 ("pos"   , ctypes.c_double * 3 ),
                 ("vel"   , ctypes.c_double * 3 ),
                 ("acc"   , ctypes.c_double * 3 ),
                 ("taun"  , ctypes.c_double ),
                 ("gamn"  , ctypes.c_double ),
                 ("dtaun" , ctypes.c_double )]
    def SetConstants(self):
        pass


class peph_t (my_endian):
    """
peph_t{        /* precise ephemeris type */
    gtime_t time;       /* time (GPST) */
    int index;          /* ephemeris index for multiple files */
    double pos[MAXSAT][4]; /* satellite position/clock (ecef) (m|s) */
    float  std[MAXSAT][4]; /* satellite position/clock std (m|s) */
    double vel[MAXSAT][4]; /* satellite velocity/clk-rate (m/s|s/s) */
    float  vst[MAXSAT][4]; /* satellite velocity/clk-rate std (m/s|s/s) */
    float  cov[MAXSAT][3]; /* satellite position covariance (m^2) */
    float  vco[MAXSAT][3]; /* satellite velocity covariance (m^2) */
} """
    _pack_ = 1

    _fields_ = [ ("time"       , gtime_t ),
                 ("index"      , ctypes.c_int ),
                 ("pad_160_32" , ctypes.c_ubyte   * 4 ),
                 ("pos"        , (ctypes.c_double * 4) * 55 ),
                 ("std"        , (ctypes.c_float  * 4) * 55 ),
                 ("vel"        , (ctypes.c_double * 4) * 55 ),
                 ("vst"        , (ctypes.c_float  * 4) * 55 ),
                 ("cov"        , (ctypes.c_float  * 3) * 55 ),
                 ("vco"        , (ctypes.c_float  * 3) * 55 )]
    def SetConstants(self):
        pass


class pclk_t (my_endian):
    """
pclk_t{        /* precise clock type */
    gtime_t time;       /* time (GPST) */
    int index;          /* clock index for multiple files */
    double clk[MAXSAT][1]; /* satellite clock (s) */
    float  std[MAXSAT][1]; /* satellite clock std (s) */
} """
    _pack_ = 1

    _fields_ = [ ("time"        , gtime_t ),
                 ("index"       , ctypes.c_int ),
                 ("pad_160_32"  , ctypes.c_ubyte   * 4 ),
                 ("clk"         , (ctypes.c_double * 1) * 55 ),
                 ("std"         , (ctypes.c_float  * 1) * 55 ),
                 ("pad_5472_32" , ctypes.c_ubyte   * 4 )]
    def SetConstants(self):
        pass


class seph_t (my_endian):
    """
seph_t{        /* SBAS ephemeris type */
    int sat;            /* satellite number */
    gtime_t t0;         /* reference epoch time (GPST) */
    gtime_t tof;        /* time of message frame (GPST) */
    int sva;            /* SV accuracy (URA index) */
    int svh;            /* SV health (0:ok) */
    double pos[3];      /* satellite position (m) (ecef) */
    double vel[3];      /* satellite velocity (m/s) (ecef) */
    double acc[3];      /* satellite acceleration (m/s^2) (ecef) */
    double af0,af1;     /* satellite clock-offset/drift (s,s/s) */
} """
    _pack_ = 1

    _fields_ = [ ("sat"       , ctypes.c_int ),
                 ("pad_32_32" , ctypes.c_ubyte  * 4 ),
                 ("t0"        , gtime_t ),
                 ("tof"       , gtime_t ),
                 ("sva"       , ctypes.c_int ),
                 ("svh"       , ctypes.c_int ),
                 ("pos"       , ctypes.c_double * 3 ),
                 ("vel"       , ctypes.c_double * 3 ),
                 ("acc"       , ctypes.c_double * 3 ),
                 ("af0"       , ctypes.c_double ),
                 ("af1"       , ctypes.c_double )]
    def SetConstants(self):
        pass


class tled_t (my_endian):
    """
tled_t{        /* norad two line element data type */
    char name [32];     /* common name */
    char alias[32];     /* alias name */
    char satno[16];     /* satellilte catalog number */
    char satclass;      /* classification */
    char desig[16];     /* international designator */
    gtime_t epoch;      /* element set epoch (UTC) */
    double ndot;        /* 1st derivative of mean motion */
    double nddot;       /* 2st derivative of mean motion */
    double bstar;       /* B* drag term */
    int etype;          /* element set type */
    int eleno;          /* element number */
    double inc;         /* orbit inclination (deg) */
    double OMG;         /* right ascension of ascending node (deg) */
    double ecc;         /* eccentricity */
    double omg;         /* argument of perigee (deg) */
    double M;           /* mean anomaly (deg) */
    double n;           /* mean motion (rev/day) */
    int rev;            /* revolution number at epoch */
} """
    _pack_ = 1

    _fields_ = [ ("name"        , ctypes.c_char  * 32 ),
                 ("alias"       , ctypes.c_char  * 32 ),
                 ("satno"       , ctypes.c_char  * 16 ),
                 ("satclass"    , ctypes.c_char ),
                 ("desig"       , ctypes.c_char  * 16 ),
                 ("pad_776_56"  , ctypes.c_ubyte * 7 ),
                 ("epoch"       , gtime_t ),
                 ("ndot"        , ctypes.c_double ),
                 ("nddot"       , ctypes.c_double ),
                 ("bstar"       , ctypes.c_double ),
                 ("etype"       , ctypes.c_int ),
                 ("eleno"       , ctypes.c_int ),
                 ("inc"         , ctypes.c_double ),
                 ("OMG"         , ctypes.c_double ),
                 ("ecc"         , ctypes.c_double ),
                 ("omg"         , ctypes.c_double ),
                 ("M"           , ctypes.c_double ),
                 ("n"           , ctypes.c_double ),
                 ("rev"         , ctypes.c_int ),
                 ("pad_1632_32" , ctypes.c_ubyte * 4 )]
    def SetConstants(self):
        pass


class tle_t (my_endian):
    """
tle_t{        /* norad two line element type */
    int n,nmax;         /* number/max number of two line element data */
    tled_t *data;       /* norad two line element data */
} """
    _pack_ = 1

    _fields_ = [ ("n"    , ctypes.c_int ),
                 ("nmax" , ctypes.c_int ),
                 ("data" , ctypes.POINTER(tled_t) )]
    def SetConstants(self):
        pass


class tec_t (my_endian):
    """
tec_t{        /* TEC grid type */
    gtime_t time;       /* epoch time (GPST) */
    int ndata[3];       /* TEC grid data size {nlat,nlon,nhgt} */
    double rb;          /* earth radius (km) */
    double lats[3];     /* latitude start/interval (deg) */
    double lons[3];     /* longitude start/interval (deg) */
    double hgts[3];     /* heights start/interval (km) */
    double *data;       /* TEC grid data (tecu) */
    float *rms;         /* RMS values (tecu) */
} """
    _pack_ = 1

    _fields_ = [ ("time"       , gtime_t ),
                 ("ndata"      , ctypes.c_int    * 3 ),
                 ("pad_224_32" , ctypes.c_ubyte  * 4 ),
                 ("rb"         , ctypes.c_double ),
                 ("lats"       , ctypes.c_double * 3 ),
                 ("lons"       , ctypes.c_double * 3 ),
                 ("hgts"       , ctypes.c_double * 3 ),
                 ("data"       , ctypes.POINTER(ctypes.c_double) ),
                 ("rms"        , ctypes.POINTER(ctypes.c_float) )]
    def SetConstants(self):
        pass


class stecd_t (my_endian):
    """
stecd_t{        /* stec data type */
    gtime_t time;       /* time (GPST) */
    unsigned char sat;  /* satellite number */
    unsigned char slip; /* slip flag */
    float iono;         /* L1 ionosphere delay (m) */
    float rate;         /* L1 ionosphere rate (m/s) */
    float rms;          /* rms value (m) */
} """
    _pack_ = 1

    _fields_ = [ ("time"       , gtime_t ),
                 ("sat"        , ctypes.c_ubyte ),
                 ("slip"       , ctypes.c_ubyte ),
                 ("pad_144_16" , ctypes.c_ubyte * 2 ),
                 ("iono"       , ctypes.c_float ),
                 ("rate"       , ctypes.c_float ),
                 ("rms"        , ctypes.c_float )]
    def SetConstants(self):
        pass


class stec_t (my_endian):
    """
stec_t{        /* stec grid type */
    double pos[2];      /* latitude/longitude (deg) */
    int index[MAXSAT];  /* search index */
    int n,nmax;         /* number of data */
    stecd_t *data;      /* stec data */
} """
    _pack_ = 1

    _fields_ = [ ("pos"         , ctypes.c_double * 2 ),
                 ("index"       , ctypes.c_int    * 55 ),
                 ("n"           , ctypes.c_int ),
                 ("nmax"        , ctypes.c_int ),
                 ("pad_1952_32" , ctypes.c_ubyte  * 4 ),
                 ("data"        , ctypes.POINTER(stecd_t) )]
    def SetConstants(self):
        pass


class zwdd_t (my_endian):
    """
zwdd_t{        /* zwd data type */
    gtime_t time;       /* time (GPST) */
    float zwd;          /* zenith wet delay (m) */
    float rms;          /* rms value (m) */
} """
    _pack_ = 1

    _fields_ = [ ("time" , gtime_t ),
                 ("zwd"  , ctypes.c_float ),
                 ("rms"  , ctypes.c_float )]
    def SetConstants(self):
        pass


class zwd_t (my_endian):
    """
zwd_t{        /* zwd grid type */
    float pos[2];       /* latitude,longitude (rad) */
    int n,nmax;         /* number of data */
    zwdd_t *data;       /* zwd data */
} """
    _pack_ = 1

    _fields_ = [ ("pos"  , ctypes.c_float * 2 ),
                 ("n"    , ctypes.c_int ),
                 ("nmax" , ctypes.c_int ),
                 ("data" , ctypes.POINTER(zwdd_t) )]
    def SetConstants(self):
        pass


class sbsmsg_t (my_endian):
    """
sbsmsg_t{        /* SBAS message type */
    int week,tow;       /* receiption time */
    int prn;            /* SBAS satellite PRN number */
    unsigned char msg[29]; /* SBAS message (226bit) padded by 0 */
} """
    _pack_ = 1

    _fields_ = [ ("week"       , ctypes.c_int ),
                 ("tow"        , ctypes.c_int ),
                 ("prn"        , ctypes.c_int ),
                 ("msg"        , ctypes.c_ubyte * 29 ),
                 ("pad_328_24" , ctypes.c_ubyte * 3 )]
    def SetConstants(self):
        pass


class sbs_t (my_endian):
    """
sbs_t{        /* SBAS messages type */
    int n,nmax;         /* number of SBAS messages/allocated */
    sbsmsg_t *msgs;     /* SBAS messages */
} """
    _pack_ = 1

    _fields_ = [ ("n"    , ctypes.c_int ),
                 ("nmax" , ctypes.c_int ),
                 ("msgs" , ctypes.POINTER(sbsmsg_t) )]
    def SetConstants(self):
        pass


class sbsfcorr_t (my_endian):
    """
sbsfcorr_t{        /* SBAS fast correction type */
    gtime_t t0;         /* time of applicability (TOF) */
    double prc;         /* pseudorange correction (PRC) (m) */
    double rrc;         /* range-rate correction (RRC) (m/s) */
    double dt;          /* range-rate correction delta-time (s) */
    int iodf;           /* IODF (issue of date fast corr) */
    short udre;         /* UDRE+1 */
    short ai;           /* degradation factor indicator */
} """
    _pack_ = 1

    _fields_ = [ ("t0"   , gtime_t ),
                 ("prc"  , ctypes.c_double ),
                 ("rrc"  , ctypes.c_double ),
                 ("dt"   , ctypes.c_double ),
                 ("iodf" , ctypes.c_int ),
                 ("udre" , ctypes.c_short ),
                 ("ai"   , ctypes.c_short )]
    def SetConstants(self):
        pass


class sbslcorr_t (my_endian):
    """
sbslcorr_t{        /* SBAS long term satellite error correction type */
    gtime_t t0;         /* correction time */
    int iode;           /* IODE (issue of date ephemeris) */
    double dpos[3];     /* delta position (m) (ecef) */
    double dvel[3];     /* delta velocity (m/s) (ecef) */
    double daf0,daf1;   /* delta clock-offset/drift (s,s/s) */
} """
    _pack_ = 1

    _fields_ = [ ("t0"         , gtime_t ),
                 ("iode"       , ctypes.c_int ),
                 ("pad_160_32" , ctypes.c_ubyte  * 4 ),
                 ("dpos"       , ctypes.c_double * 3 ),
                 ("dvel"       , ctypes.c_double * 3 ),
                 ("daf0"       , ctypes.c_double ),
                 ("daf1"       , ctypes.c_double )]
    def SetConstants(self):
        pass


class sbssatp_t (my_endian):
    """
sbssatp_t{        /* SBAS satellite correction type */
    int sat;            /* satellite number */
    sbsfcorr_t fcorr;   /* fast correction */
    sbslcorr_t lcorr;   /* long term correction */
} """
    _pack_ = 1

    _fields_ = [ ("sat"       , ctypes.c_int ),
                 ("pad_32_32" , ctypes.c_ubyte * 4 ),
                 ("fcorr"     , sbsfcorr_t ),
                 ("lcorr"     , sbslcorr_t )]
    def SetConstants(self):
        pass


class sbssat_t (my_endian):
    """
sbssat_t {        /* SBAS satellite corrections type */
    int iodp;           /* IODP (issue of date mask) */
    int nsat;           /* number of satellites */
    int tlat;           /* system latency (s) */
    sbssatp_t sat[MAXSAT]; /* satellite correction */
 }  """
    _pack_ = 1

    _fields_ = [ ("iodp"      , ctypes.c_int ),
                 ("nsat"      , ctypes.c_int ),
                 ("tlat"      , ctypes.c_int ),
                 ("pad_96_32" , ctypes.c_ubyte * 4 ),
                 ("sat"       , sbssatp_t      * 55 )]
    def SetConstants(self):
        pass


class sbsigp_t (my_endian):
    """
sbsigp_t {        /* SBAS ionospheric correction type */
    gtime_t t0;         /* correction time */
    short lat,lon;      /* latitude/longitude (deg) */
    short give;         /* GIVI+1 */
    float delay;        /* vertical delay estimate (m) */
 }  """
    _pack_ = 1

    _fields_ = [ ("t0"         , gtime_t ),
                 ("lat"        , ctypes.c_short ),
                 ("lon"        , ctypes.c_short ),
                 ("give"       , ctypes.c_short ),
                 ("pad_176_16" , ctypes.c_ubyte * 2 ),
                 ("delay"      , ctypes.c_float ),
                 ("pad_224_32" , ctypes.c_ubyte * 4 )]
    def SetConstants(self):
        pass


class sbsigpband_t (my_endian):
    """
sbsigpband_t{        /* IGP band type */
    short x;            /* longitude/latitude (deg) */
    const short *y;     /* latitudes/longitudes (deg) */
    unsigned char bits; /* IGP mask start bit */
    unsigned char bite; /* IGP mask end bit */
} """
    _pack_ = 1

    _fields_ = [ ("x"          , ctypes.c_short ),
                 ("pad_16_48"  , ctypes.c_ubyte * 6 ),
                 ("y"          , ctypes.POINTER(ctypes.c_int64) ),
                 ("bits"       , ctypes.c_ubyte ),
                 ("bite"       , ctypes.c_ubyte ),
                 ("pad_144_48" , ctypes.c_ubyte * 6 )]
    def SetConstants(self):
        pass


class sbsion_t (my_endian):
    """
sbsion_t{        /* SBAS ionospheric corrections type */
    int iodi;           /* IODI (issue of date ionos corr) */
    int nigp;           /* number of igps */
    sbsigp_t igp[MAXNIGP]; /* ionospheric correction */
} """
    _pack_ = 1

    _fields_ = [ ("iodi" , ctypes.c_int ),
                 ("nigp" , ctypes.c_int ),
                 ("igp"  , sbsigp_t * 201 )]
    def SetConstants(self):
        pass


class dgps_t (my_endian):
    """
dgps_t{        /* DGPS/GNSS correction type */
    gtime_t t0;         /* correction time */
    double prc;         /* pseudorange correction (PRC) (m) */
    double rrc;         /* range rate correction (RRC) (m/s) */
    int iod;            /* issue of data (IOD) */
    double udre;        /* UDRE */
} """
    _pack_ = 1

    _fields_ = [ ("t0"         , gtime_t ),
                 ("prc"        , ctypes.c_double ),
                 ("rrc"        , ctypes.c_double ),
                 ("iod"        , ctypes.c_int ),
                 ("pad_288_32" , ctypes.c_ubyte * 4 ),
                 ("udre"       , ctypes.c_double )]
    def SetConstants(self):
        pass


class ssr_t (my_endian):
    """
ssr_t{        /* SSR correction type */
    gtime_t t0[5];      /* epoch time (GPST) {eph,clk,hrclk,ura,bias} */
    double udi[5];      /* SSR update interval (s) */
    int iod[5];         /* iod ssr {eph,clk,hrclk,ura,bias} */
    int iode;           /* issue of data */
    int ura;            /* URA indicator */
    int refd;           /* sat ref datum (0:ITRF,1:regional) */
    double deph [3];    /* delta orbit {radial,along,cross} (m) */
    double ddeph[3];    /* dot delta orbit {radial,along,cross} (m/s) */
    double dclk [3];    /* delta clock {c0,c1,c2} (m,m/s,m/s^2) */
    double hrclk;       /* high-rate clock corection (m) */
    float cbias[MAXCODE]; /* code biases (m) */
    unsigned char update; /* update flag (0:no update,1:update) */
} """
    _pack_ = 1

    _fields_ = [ ("t0"          , gtime_t         * 5 ),
                 ("udi"         , ctypes.c_double * 5 ),
                 ("iod"         , ctypes.c_int    * 5 ),
                 ("iode"        , ctypes.c_int ),
                 ("ura"         , ctypes.c_int ),
                 ("refd"        , ctypes.c_int ),
                 ("deph"        , ctypes.c_double * 3 ),
                 ("ddeph"       , ctypes.c_double * 3 ),
                 ("dclk"        , ctypes.c_double * 3 ),
                 ("hrclk"       , ctypes.c_double ),
                 ("cbias"       , ctypes.c_float  * 48 ),
                 ("update"      , ctypes.c_ubyte ),
                 ("pad_3400_56" , ctypes.c_ubyte  * 7 )]
    def SetConstants(self):
        pass


class lexmsg_t (my_endian):
    """
lexmsg_t{        /* QZSS LEX message type */
    int prn;            /* satellite PRN number */
    int type;           /* message type */
    int alert;          /* alert flag */
    unsigned char stat; /* signal tracking status */
    unsigned char snr;  /* signal C/N0 (0.25 dBHz) */
    unsigned int ttt;   /* tracking time (ms) */
    unsigned char msg[212]; /* LEX message data part 1695 bits */
} """
    _pack_ = 1

    _fields_ = [ ("prn"        , ctypes.c_int ),
                 ("type"       , ctypes.c_int ),
                 ("alert"      , ctypes.c_int ),
                 ("stat"       , ctypes.c_ubyte ),
                 ("snr"        , ctypes.c_ubyte ),
                 ("pad_112_16" , ctypes.c_ubyte * 2 ),
                 ("ttt"        , ctypes.c_uint ),
                 ("msg"        , ctypes.c_ubyte * 212 )]
    def SetConstants(self):
        pass


class lex_t (my_endian):
    """
lex_t{        /* QZSS LEX messages type */
    int n,nmax;         /* number of LEX messages and allocated */
    lexmsg_t *msgs;     /* LEX messages */
} """
    _pack_ = 1

    _fields_ = [ ("n"    , ctypes.c_int ),
                 ("nmax" , ctypes.c_int ),
                 ("msgs" , ctypes.POINTER(lexmsg_t) )]
    def SetConstants(self):
        pass


class lexeph_t (my_endian):
    """
lexeph_t{        /* QZSS LEX ephemeris type */
    gtime_t toe;        /* epoch time (GPST) */
    gtime_t tof;        /* message frame time (GPST) */
    int sat;            /* satellite number */
    unsigned char health; /* signal health (L1,L2,L1C,L5,LEX) */
    unsigned char ura;  /* URA index */
    double pos[3];      /* satellite position (m) */
    double vel[3];      /* satellite velocity (m/s) */
    double acc[3];      /* satellite acceleration (m/s2) */
    double jerk[3];     /* satellite jerk (m/s3) */
    double af0,af1;     /* satellite clock bias and drift (s,s/s) */
    double tgd;         /* TGD */
    double isc[8];      /* ISC */
} """
    _pack_ = 1

    _fields_ = [ ("toe"        , gtime_t ),
                 ("tof"        , gtime_t ),
                 ("sat"        , ctypes.c_int ),
                 ("health"     , ctypes.c_ubyte ),
                 ("ura"        , ctypes.c_ubyte ),
                 ("pad_304_16" , ctypes.c_ubyte  * 2 ),
                 ("pos"        , ctypes.c_double * 3 ),
                 ("vel"        , ctypes.c_double * 3 ),
                 ("acc"        , ctypes.c_double * 3 ),
                 ("jerk"       , ctypes.c_double * 3 ),
                 ("af0"        , ctypes.c_double ),
                 ("af1"        , ctypes.c_double ),
                 ("tgd"        , ctypes.c_double ),
                 ("isc"        , ctypes.c_double * 8 )]
    def SetConstants(self):
        pass


class lexion_t (my_endian):
    """
lexion_t{        /* QZSS LEX ionosphere correction type */
    gtime_t t0;         /* epoch time (GPST) */
    double tspan;       /* valid time span (s) */
    double pos0[2];     /* reference position {lat,lon} (rad) */
    double coef[3][2];  /* coefficients lat x lon (3 x 2) */
} """
    _pack_ = 1

    _fields_ = [ ("t0"    , gtime_t ),
                 ("tspan" , ctypes.c_double ),
                 ("pos0"  , ctypes.c_double  * 2 ),
                 ("coef"  , (ctypes.c_double * 2) * 3 )]
    def SetConstants(self):
        pass


class nav_t (my_endian):
    """
nav_t{        /* navigation data type */
    int n,nmax;         /* number of broadcast ephemeris */
    int ng,ngmax;       /* number of glonass ephemeris */
    int ns,nsmax;       /* number of sbas ephemeris */
    int ne,nemax;       /* number of precise ephemeris */
    int nc,ncmax;       /* number of precise clock */
    int na,namax;       /* number of almanac data */
    int nt,ntmax;       /* number of tec grid data */
    int nn,nnmax;       /* number of stec grid data */
    eph_t *eph;         /* GPS/QZS/GAL ephemeris */
    geph_t *geph;       /* GLONASS ephemeris */
    seph_t *seph;       /* SBAS ephemeris */
    peph_t *peph;       /* precise ephemeris */
    pclk_t *pclk;       /* precise clock */
    alm_t *alm;         /* almanac data */
    tec_t *tec;         /* tec grid data */
    stec_t *stec;       /* stec grid data */
    erp_t  erp;         /* earth rotation parameters */
    double utc_gps[4];  /* GPS delta-UTC parameters {A0,A1,T,W} */
    double utc_glo[4];  /* GLONASS UTC GPS time parameters */
    double utc_gal[4];  /* Galileo UTC GPS time parameters */
    double utc_qzs[4];  /* QZS UTC GPS time parameters */
    double utc_cmp[4];  /* BeiDou UTC parameters */
    double utc_sbs[4];  /* SBAS UTC parameters */
    double ion_gps[8];  /* GPS iono model parameters {a0,a1,a2,a3,b0,b1,b2,b3} */
    double ion_gal[4];  /* Galileo iono model parameters {ai0,ai1,ai2,0} */
    double ion_qzs[8];  /* QZSS iono model parameters {a0,a1,a2,a3,b0,b1,b2,b3} */
    double ion_cmp[8];  /* BeiDou iono model parameters {a0,a1,a2,a3,b0,b1,b2,b3} */
    int leaps;          /* leap seconds (s) */
    double lam[MAXSAT][NFREQ]; /* carrier wave lengths (m) */
    double cbias[MAXSAT][3];   /* code bias (0:p1-p2,1:p1-c1,2:p2-c2) (m) */
    double wlbias[MAXSAT];     /* wide-lane bias (cycle) */
    double glo_cpbias[4];    /* glonass code-phase bias {1C,1P,2C,2P} (m) */
    char glo_fcn[MAXPRNGLO+1]; /* glonass frequency channel number + 8 */
    pcv_t pcvs[MAXSAT]; /* satellite antenna pcv */
    sbssat_t sbssat;    /* SBAS satellite corrections */
    sbsion_t sbsion[MAXBAND+1]; /* SBAS ionosphere corrections */
    dgps_t dgps[MAXSAT]; /* DGPS corrections */
    ssr_t ssr[MAXSAT];  /* SSR corrections */
    lexeph_t lexeph[MAXSAT]; /* LEX ephemeris */
    lexion_t lexion;    /* LEX ionosphere correction */
} """
    _pack_ = 1

    _fields_ = [ ("n"            , ctypes.c_int ),
                 ("nmax"         , ctypes.c_int ),
                 ("ng"           , ctypes.c_int ),
                 ("ngmax"        , ctypes.c_int ),
                 ("ns"           , ctypes.c_int ),
                 ("nsmax"        , ctypes.c_int ),
                 ("ne"           , ctypes.c_int ),
                 ("nemax"        , ctypes.c_int ),
                 ("nc"           , ctypes.c_int ),
                 ("ncmax"        , ctypes.c_int ),
                 ("na"           , ctypes.c_int ),
                 ("namax"        , ctypes.c_int ),
                 ("nt"           , ctypes.c_int ),
                 ("ntmax"        , ctypes.c_int ),
                 ("nn"           , ctypes.c_int ),
                 ("nnmax"        , ctypes.c_int ),
                 ("eph"          , ctypes.POINTER(eph_t) ),
                 ("geph"         , ctypes.POINTER(geph_t) ),
                 ("seph"         , ctypes.POINTER(seph_t) ),
                 ("peph"         , ctypes.POINTER(peph_t) ),
                 ("pclk"         , ctypes.POINTER(pclk_t) ),
                 ("alm"          , ctypes.POINTER(alm_t) ),
                 ("tec"          , ctypes.POINTER(tec_t) ),
                 ("stec"         , ctypes.POINTER(stec_t) ),
                 ("erp"          , erp_t ),
                 ("utc_gps"      , ctypes.c_double  * 4 ),
                 ("utc_glo"      , ctypes.c_double  * 4 ),
                 ("utc_gal"      , ctypes.c_double  * 4 ),
                 ("utc_qzs"      , ctypes.c_double  * 4 ),
                 ("utc_cmp"      , ctypes.c_double  * 4 ),
                 ("utc_sbs"      , ctypes.c_double  * 4 ),
                 ("ion_gps"      , ctypes.c_double  * 8 ),
                 ("ion_gal"      , ctypes.c_double  * 4 ),
                 ("ion_qzs"      , ctypes.c_double  * 8 ),
                 ("ion_cmp"      , ctypes.c_double  * 8 ),
                 ("leaps"        , ctypes.c_int ),
                 ("pad_4512_32"  , ctypes.c_ubyte   * 4 ),
                 ("lam"          , (ctypes.c_double * 3) * 55 ),
                 ("cbias"        , (ctypes.c_double * 3) * 55 ),
                 ("wlbias"       , ctypes.c_double  * 55 ),
                 ("glo_cpbias"   , ctypes.c_double  * 4 ),
                 ("glo_fcn"      , ctypes.c_char    * 1 ),
                 ("pad_29448_56" , ctypes.c_ubyte   * 7 ),
                 ("pcvs"         , pcv_t            * 55 ),
                 ("sbssat"       , sbssat_t ),
                 ("sbsion"       , sbsion_t         * 11 ),
                 ("dgps"         , dgps_t           * 55 ),
                 ("ssr"          , ssr_t            * 55 ),
                 ("lexeph"       , lexeph_t         * 55 ),
                 ("lexion"       , lexion_t )]
    def SetConstants(self):
        pass


class sta_t (my_endian):
    """
sta_t{        /* station parameter type */
    char name   [MAXANT]; /* marker name */
    char marker [MAXANT]; /* marker number */
    char antdes [MAXANT]; /* antenna descriptor */
    char antsno [MAXANT]; /* antenna serial number */
    char rectype[MAXANT]; /* receiver type descriptor */
    char recver [MAXANT]; /* receiver firmware version */
    char recsno [MAXANT]; /* receiver serial number */
    int antsetup;       /* antenna setup id */
    int itrf;           /* ITRF realization year */
    int deltype;        /* antenna delta type (0:enu,1:xyz) */
    double pos[3];      /* station position (ecef) (m) */
    double del[3];      /* antenna position delta (e/n/u or x/y/z) (m) */
    double hgt;         /* antenna height (m) */
} """
    _pack_ = 1

    _fields_ = [ ("name"        , ctypes.c_char   * 64 ),
                 ("marker"      , ctypes.c_char   * 64 ),
                 ("antdes"      , ctypes.c_char   * 64 ),
                 ("antsno"      , ctypes.c_char   * 64 ),
                 ("rectype"     , ctypes.c_char   * 64 ),
                 ("recver"      , ctypes.c_char   * 64 ),
                 ("recsno"      , ctypes.c_char   * 64 ),
                 ("antsetup"    , ctypes.c_int ),
                 ("itrf"        , ctypes.c_int ),
                 ("deltype"     , ctypes.c_int ),
                 ("pad_3680_32" , ctypes.c_ubyte  * 4 ),
                 ("pos"         , ctypes.c_double * 3 ),
                 ("del"         , ctypes.c_double * 3 ),
                 ("hgt"         , ctypes.c_double )]
    def SetConstants(self):
        pass


class sol_t (my_endian):
    """
sol_t{        /* solution type */
    gtime_t time;       /* time (GPST) */
    double rr[6];       /* position/velocity (m|m/s) */
                        /* {x,y,z,vx,vy,vz} or {e,n,u,ve,vn,vu} */
    float  qr[6];       /* position variance/covariance (m^2) */
                        /* {c_xx,c_yy,c_zz,c_xy,c_yz,c_zx} or */
                        /* {c_ee,c_nn,c_uu,c_en,c_nu,c_ue} */
    double dtr[6];      /* receiver clock bias to time systems (s) */
    unsigned char type; /* type (0:xyz-ecef,1:enu-baseline) */
    unsigned char stat; /* solution status (SOLQ_???) */
    unsigned char ns;   /* number of valid satellites */
    float age;          /* age of differential (s) */
    float ratio;        /* AR ratio factor for valiation */
} """
    _pack_ = 1

    _fields_ = [ ("time"        , gtime_t ),
                 ("rr"          , ctypes.c_double * 6 ),
                 ("qr"          , ctypes.c_float  * 6 ),
                 ("dtr"         , ctypes.c_double * 6 ),
                 ("type"        , ctypes.c_ubyte ),
                 ("stat"        , ctypes.c_ubyte ),
                 ("ns"          , ctypes.c_ubyte ),
                 ("pad_1112_8"  , ctypes.c_ubyte ),
                 ("age"         , ctypes.c_float ),
                 ("ratio"       , ctypes.c_float ),
                 ("pad_1184_32" , ctypes.c_ubyte  * 4 )]
    def SetConstants(self):
        pass


class solbuf_t (my_endian):
    """
solbuf_t{        /* solution buffer type */
    int n,nmax;         /* number of solution/max number of buffer */
    int cyclic;         /* cyclic buffer flag */
    int start,end;      /* start/end index */
    gtime_t time;       /* current solution time */
    sol_t *data;        /* solution data */
    double rb[3];       /* reference position {x,y,z} (ecef) (m) */
    unsigned char buff[MAXSOLMSG+1]; /* message buffer */
    int nb;             /* number of byte in message buffer */
} """
    _pack_ = 1

    _fields_ = [ ("n"            , ctypes.c_int ),
                 ("nmax"         , ctypes.c_int ),
                 ("cyclic"       , ctypes.c_int ),
                 ("start"        , ctypes.c_int ),
                 ("end"          , ctypes.c_int ),
                 ("pad_160_32"   , ctypes.c_ubyte  * 4 ),
                 ("time"         , gtime_t ),
                 ("data"         , ctypes.POINTER(sol_t) ),
                 ("rb"           , ctypes.c_double * 3 ),
                 ("buff"         , ctypes.c_ubyte  * 4097 ),
                 ("pad_33352_24" , ctypes.c_ubyte  * 3 ),
                 ("nb"           , ctypes.c_int )]
    def SetConstants(self):
        pass


class solstat_t (my_endian):
    """
solstat_t{        /* solution status type */
    gtime_t time;       /* time (GPST) */
    unsigned char sat;  /* satellite number */
    unsigned char frq;  /* frequency (1:L1,2:L2,...) */
    float az,el;        /* azimuth/elevation angle (rad) */
    float resp;         /* pseudorange residual (m) */
    float resc;         /* carrier-phase residual (m) */
    unsigned char flag; /* flags: (vsat<<5)+(slip<<3)+fix */
    unsigned char snr;  /* signal strength (0.25 dBHz) */
    unsigned short lock;  /* lock counter */
    unsigned short outc;  /* outage counter */
    unsigned short slipc; /* slip counter */
    unsigned short rejc;  /* reject counter */
} """
    _pack_ = 1

    _fields_ = [ ("time"       , gtime_t ),
                 ("sat"        , ctypes.c_ubyte ),
                 ("frq"        , ctypes.c_ubyte ),
                 ("pad_144_16" , ctypes.c_ubyte * 2 ),
                 ("az"         , ctypes.c_float ),
                 ("el"         , ctypes.c_float ),
                 ("resp"       , ctypes.c_float ),
                 ("resc"       , ctypes.c_float ),
                 ("flag"       , ctypes.c_ubyte ),
                 ("snr"        , ctypes.c_ubyte ),
                 ("lock"       , ctypes.c_ushort ),
                 ("outc"       , ctypes.c_ushort ),
                 ("slipc"      , ctypes.c_ushort ),
                 ("rejc"       , ctypes.c_ushort ),
                 ("pad_368_16" , ctypes.c_ubyte * 2 )]
    def SetConstants(self):
        pass


class solstatbuf_t (my_endian):
    """
solstatbuf_t{        /* solution status buffer type */
    int n,nmax;         /* number of solution/max number of buffer */
    solstat_t *data;    /* solution status data */
} """
    _pack_ = 1

    _fields_ = [ ("n"    , ctypes.c_int ),
                 ("nmax" , ctypes.c_int ),
                 ("data" , ctypes.POINTER(solstat_t) )]
    def SetConstants(self):
        pass


class rtcm_t (my_endian):
    """
rtcm_t{        /* RTCM control struct type */
    int staid;          /* station id */
    int stah;           /* station health */
    int seqno;          /* sequence number for rtcm 2 or iods msm */
    int outtype;        /* output message type */
    gtime_t time;       /* message time */
    gtime_t time_s;     /* message start time */
    obs_t obs;          /* observation data (uncorrected) */
    nav_t nav;          /* satellite ephemerides */
    sta_t sta;          /* station parameters */
    dgps_t *dgps;       /* output of dgps corrections */
    ssr_t ssr[MAXSAT];  /* output of ssr corrections */
    char msg[128];      /* special message */
    char msgtype[256];  /* last message type */
    char msmtype[6][128]; /* msm signal types */
    int obsflag;        /* obs data complete flag (1:ok,0:not complete) */
    int ephsat;         /* update satellite of ephemeris */
    double cp[MAXSAT][NFREQ+NEXOBS]; /* carrier-phase measurement */
    unsigned char lock[MAXSAT][NFREQ+NEXOBS]; /* lock time */
    unsigned char loss[MAXSAT][NFREQ+NEXOBS]; /* loss of lock count */
    gtime_t lltime[MAXSAT][NFREQ+NEXOBS]; /* last lock time */
    int nbyte;          /* number of bytes in message buffer */ 
    int nbit;           /* number of bits in word buffer */ 
    int len;            /* message length (bytes) */
    unsigned char buff[1200]; /* message buffer */
    unsigned int word;  /* word buffer for rtcm 2 */
    unsigned int nmsg2[100]; /* message count of RTCM 2 (1-99:1-99,0:other) */
    unsigned int nmsg3[300]; /* message count of RTCM 3 (1-299:1001-1299,0:ohter) */
    char opt[256];      /* RTCM dependent options */
} """
    _pack_ = 1

    _fields_ = [ ("staid"          , ctypes.c_int ),
                 ("stah"           , ctypes.c_int ),
                 ("seqno"          , ctypes.c_int ),
                 ("outtype"        , ctypes.c_int ),
                 ("time"           , gtime_t ),
                 ("time_s"         , gtime_t ),
                 ("obs"            , obs_t ),
                 ("nav"            , nav_t ),
                 ("sta"            , sta_t ),
                 ("dgps"           , ctypes.POINTER(dgps_t) ),
                 ("ssr"            , ssr_t            * 55 ),
                 ("msg"            , ctypes.c_char    * 128 ),
                 ("msgtype"        , ctypes.c_char    * 256 ),
                 ("msmtype"        , (ctypes.c_char   * 128) * 6 ),
                 ("obsflag"        , ctypes.c_int ),
                 ("ephsat"         , ctypes.c_int ),
                 ("cp"             , (ctypes.c_double * 3) * 55 ),
                 ("lock"           , (ctypes.c_ubyte  * 3) * 55 ),
                 ("loss"           , (ctypes.c_ubyte  * 3) * 55 ),
                 ("pad_1493712_48" , ctypes.c_ubyte   * 6 ),
                 ("lltime"         , (gtime_t         * 3) * 55 ),
                 ("nbyte"          , ctypes.c_int ),
                 ("nbit"           , ctypes.c_int ),
                 ("len"            , ctypes.c_int ),
                 ("buff"           , ctypes.c_ubyte   * 1200 ),
                 ("word"           , ctypes.c_uint ),
                 ("nmsg2"          , ctypes.c_uint    * 100 ),
                 ("nmsg3"          , ctypes.c_uint    * 300 ),
                 ("opt"            , ctypes.c_char    * 256 )]
    def SetConstants(self):
        pass


class rnxctr_t (my_endian):
    """
rnxctr_t{        /* rinex control struct type */
    gtime_t time;       /* message time */
    double ver;         /* rinex version */
    char   type;        /* rinex file type ('O','N',...) */
    int    sys;         /* navigation system */
    int    tsys;        /* time system */
    char   tobs[6][MAXOBSTYPE][4]; /* rinex obs types */
    obs_t  obs;         /* observation data */
    nav_t  nav;         /* navigation data */
    sta_t  sta;         /* station info */
    int    ephsat;      /* ephemeris satellite number */
    char   opt[256];    /* rinex dependent options */
} """
    _pack_ = 1

    _fields_ = [ ("time"           , gtime_t ),
                 ("ver"            , ctypes.c_double ),
                 ("type"           , ctypes.c_char ),
                 ("pad_200_24"     , ctypes.c_ubyte  * 3 ),
                 ("sys"            , ctypes.c_int ),
                 ("tsys"           , ctypes.c_int ),
                 ("tobs"           , ((ctypes.c_char * 4) * 64) * 6 ),
                 ("pad_12576_32"   , ctypes.c_ubyte  * 4 ),
                 ("obs"            , obs_t ),
                 ("nav"            , nav_t ),
                 ("sta"            , sta_t ),
                 ("ephsat"         , ctypes.c_int ),
                 ("opt"            , ctypes.c_char   * 256 ),
                 ("pad_1295392_32" , ctypes.c_ubyte  * 4 )]
    def SetConstants(self):
        pass


class url_t (my_endian):
    """
url_t{        /* download url type */
    char type[32];      /* data type */
    char path[1024];    /* url path */
    char dir [1024];    /* local directory */
    double tint;        /* time interval (s) */
} """
    _pack_ = 1

    _fields_ = [ ("type" , ctypes.c_char * 32 ),
                 ("path" , ctypes.c_char * 1024 ),
                 ("dir"  , ctypes.c_char * 1024 ),
                 ("tint" , ctypes.c_double )]
    def SetConstants(self):
        pass


class opt_t (my_endian):
    """
opt_t{        /* option type */
    char *name;         /* option name */
    int format;         /* option format (0:int,1:double,2:string,3:enum) */
    void *var;          /* pointer to option variable */
    char *comment;      /* option comment/enum labels/unit */
} """
    _pack_ = 1

    _fields_ = [ ("name"      , ctypes.POINTER(ctypes.c_char) ),
                 ("format"    , ctypes.c_int ),
                 ("pad_96_32" , ctypes.c_ubyte * 4 ),
                 ("var"       , ctypes.POINTER(None) ),
                 ("comment"   , ctypes.POINTER(ctypes.c_char) )]
    def SetConstants(self):
        pass


class exterr_t (my_endian):
    """
exterr_t{        /* extended receiver error model */
    int ena[4];         /* model enabled */
    double cerr[4][NFREQ*2]; /* code errors (m) */
    double perr[4][NFREQ*2]; /* carrier-phase errors (m) */
    double gpsglob[NFREQ]; /* gps-glonass h/w bias (m) */
    double gloicb [NFREQ]; /* glonass interchannel bias (m/fn) */
} """
    _pack_ = 1

    _fields_ = [ ("ena"     , ctypes.c_int     * 4 ),
                 ("cerr"    , (ctypes.c_double * 6) * 4 ),
                 ("perr"    , (ctypes.c_double * 6) * 4 ),
                 ("gpsglob" , ctypes.c_double  * 3 ),
                 ("gloicb"  , ctypes.c_double  * 3 )]
    def SetConstants(self):
        pass


class snrmask_t (my_endian):
    """
snrmask_t{        /* SNR mask type */
    int ena[2];         /* enable flag {rover,base} */
    double mask[NFREQ][9]; /* mask (dBHz) at 5,10,...85 deg */
} """
    _pack_ = 1

    _fields_ = [ ("ena"  , ctypes.c_int     * 2 ),
                 ("mask" , (ctypes.c_double * 9) * 3 )]
    def SetConstants(self):
        pass


class prcopt_t (my_endian):
    """
prcopt_t{        /* processing options type */
    int mode;           /* positioning mode (PMODE_???) */
    int soltype;        /* solution type (0:forward,1:backward,2:combined) */
    int nf;             /* number of frequencies (1:L1,2:L1+L2,3:L1+L2+L5) */
    int navsys;         /* navigation system */
    double elmin;       /* elevation mask angle (rad) */
    snrmask_t snrmask;  /* SNR mask */
    int sateph;         /* satellite ephemeris/clock (EPHOPT_???) */
    int modear;         /* AR mode (0:off,1:continuous,2:instantaneous,3:fix and hold,4:ppp-ar) */
    int glomodear;      /* GLONASS AR mode (0:off,1:on,2:auto cal,3:ext cal) */
    int maxout;         /* obs outage count to reset bias */
    int minlock;        /* min lock count to fix ambiguity */
    int minfix;         /* min fix count to hold ambiguity */
    int ionoopt;        /* ionosphere option (IONOOPT_???) */
    int tropopt;        /* troposphere option (TROPOPT_???) */
    int dynamics;       /* dynamics model (0:none,1:velociy,2:accel) */
    int tidecorr;       /* earth tide correction (0:off,1:solid,2:solid+otl+pole) */
    int niter;          /* number of filter iteration */
    int codesmooth;     /* code smoothing window size (0:none) */
    int intpref;        /* interpolate reference obs (for post mission) */
    int sbascorr;       /* SBAS correction options */
    int sbassatsel;     /* SBAS satellite selection (0:all) */
    int rovpos;         /* rover position for fixed mode */
    int refpos;         /* base position for relative mode */
                        /* (0:pos in prcopt,  1:average of single pos, */
                        /*  2:read from file, 3:rinex header, 4:rtcm pos) */
    double eratio[NFREQ]; /* code/phase error ratio */
    double err[5];      /* measurement error factor */
                        /* [0]:reserved */
                        /* [1-3]:error factor a/b/c of phase (m) */
                        /* [4]:doppler frequency (hz) */
    double std[3];      /* initial-state std [0]bias,[1]iono [2]trop */
    double prn[5];      /* process-noise std [0]bias,[1]iono [2]trop [3]acch [4]accv */
    double sclkstab;    /* satellite clock stability (sec/sec) */
    double thresar[4];  /* AR validation threshold */
    double elmaskar;    /* elevation mask of AR for rising satellite (deg) */
    double elmaskhold;  /* elevation mask to hold ambiguity (deg) */
    double thresslip;   /* slip threshold of geometry-free phase (m) */
    double maxtdiff;    /* max difference of time (sec) */
    double maxinno;     /* reject threshold of innovation (m) */
    double maxgdop;     /* reject threshold of gdop */
    double baseline[2]; /* baseline length constraint {const,sigma} (m) */
    double ru[3];       /* rover position for fixed mode {x,y,z} (ecef) (m) */
    double rb[3];       /* base position for relative mode {x,y,z} (ecef) (m) */
    char anttype[2][MAXANT]; /* antenna types {rover,base} */
    double antdel[2][3]; /* antenna delta {{rov_e,rov_n,rov_u},{ref_e,ref_n,ref_u}} */
    pcv_t pcvr[2];      /* receiver antenna parameters {rov,base} */
    unsigned char exsats[MAXSAT]; /* excluded satellites (1:excluded,2:included) */
    char rnxopt[2][256]; /* rinex options {rover,base} */
    int  posopt[6];     /* positioning options */
    int  syncsol;       /* solution sync mode (0:off,1:on) */
    double odisp[2][6*11]; /* ocean tide loading parameters {rov,base} */
    exterr_t exterr;    /* extended receiver error model */
} """
    _pack_ = 1

    _fields_ = [ ("mode"         , ctypes.c_int ),
                 ("soltype"      , ctypes.c_int ),
                 ("nf"           , ctypes.c_int ),
                 ("navsys"       , ctypes.c_int ),
                 ("elmin"        , ctypes.c_double ),
                 ("snrmask"      , snrmask_t ),
                 ("sateph"       , ctypes.c_int ),
                 ("modear"       , ctypes.c_int ),
                 ("glomodear"    , ctypes.c_int ),
                 ("maxout"       , ctypes.c_int ),
                 ("minlock"      , ctypes.c_int ),
                 ("minfix"       , ctypes.c_int ),
                 ("ionoopt"      , ctypes.c_int ),
                 ("tropopt"      , ctypes.c_int ),
                 ("dynamics"     , ctypes.c_int ),
                 ("tidecorr"     , ctypes.c_int ),
                 ("niter"        , ctypes.c_int ),
                 ("codesmooth"   , ctypes.c_int ),
                 ("intpref"      , ctypes.c_int ),
                 ("sbascorr"     , ctypes.c_int ),
                 ("sbassatsel"   , ctypes.c_int ),
                 ("rovpos"       , ctypes.c_int ),
                 ("refpos"       , ctypes.c_int ),
                 ("pad_2528_32"  , ctypes.c_ubyte   * 4 ),
                 ("eratio"       , ctypes.c_double  * 3 ),
                 ("err"          , ctypes.c_double  * 5 ),
                 ("std"          , ctypes.c_double  * 3 ),
                 ("prn"          , ctypes.c_double  * 5 ),
                 ("sclkstab"     , ctypes.c_double ),
                 ("thresar"      , ctypes.c_double  * 4 ),
                 ("elmaskar"     , ctypes.c_double ),
                 ("elmaskhold"   , ctypes.c_double ),
                 ("thresslip"    , ctypes.c_double ),
                 ("maxtdiff"     , ctypes.c_double ),
                 ("maxinno"      , ctypes.c_double ),
                 ("maxgdop"      , ctypes.c_double ),
                 ("baseline"     , ctypes.c_double  * 2 ),
                 ("ru"           , ctypes.c_double  * 3 ),
                 ("rb"           , ctypes.c_double  * 3 ),
                 ("anttype"      , (ctypes.c_char   * 64) * 2 ),
                 ("antdel"       , (ctypes.c_double * 3) * 2 ),
                 ("pcvr"         , pcv_t            * 2 ),
                 ("exsats"       , ctypes.c_ubyte   * 55 ),
                 ("rnxopt"       , (ctypes.c_char   * 256) * 2 ),
                 ("pad_21880_8"  , ctypes.c_ubyte ),
                 ("posopt"       , ctypes.c_int     * 6 ),
                 ("syncsol"      , ctypes.c_int ),
                 ("pad_22112_32" , ctypes.c_ubyte   * 4 ),
                 ("odisp"        , (ctypes.c_double * 66) * 2 ),
                 ("exterr"       , exterr_t )]
    def SetConstants(self):
        pass


class solopt_t (my_endian):
    """
solopt_t{        /* solution options type */
    int posf;           /* solution format (SOLF_???) */
    int times;          /* time system (TIMES_???) */
    int timef;          /* time format (0:sssss.s,1:yyyy/mm/dd hh:mm:ss.s) */
    int timeu;          /* time digits under decimal point */
    int degf;           /* latitude/longitude format (0:ddd.ddd,1:ddd mm ss) */
    int outhead;        /* output header (0:no,1:yes) */
    int outopt;         /* output processing options (0:no,1:yes) */
    int datum;          /* datum (0:WGS84,1:Tokyo) */
    int height;         /* height (0:ellipsoidal,1:geodetic) */
    int geoid;          /* geoid model (0:EGM96,1:JGD2000) */
    int solstatic;      /* solution of static mode (0:all,1:single) */
    int sstat;          /* solution statistics level (0:off,1:states,2:residuals) */
    int trace;          /* debug trace level (0:off,1-5:debug) */
    double nmeaintv[2]; /* nmea output interval (s) (<0:no,0:all) */
                        /* nmeaintv[0]:gprmc,gpgga,nmeaintv[1]:gpgsv */
    char sep[64];       /* field separator */
    char prog[64];      /* program name */
} """
    _pack_ = 1

    _fields_ = [ ("posf"       , ctypes.c_int ),
                 ("times"      , ctypes.c_int ),
                 ("timef"      , ctypes.c_int ),
                 ("timeu"      , ctypes.c_int ),
                 ("degf"       , ctypes.c_int ),
                 ("outhead"    , ctypes.c_int ),
                 ("outopt"     , ctypes.c_int ),
                 ("datum"      , ctypes.c_int ),
                 ("height"     , ctypes.c_int ),
                 ("geoid"      , ctypes.c_int ),
                 ("solstatic"  , ctypes.c_int ),
                 ("sstat"      , ctypes.c_int ),
                 ("trace"      , ctypes.c_int ),
                 ("pad_416_32" , ctypes.c_ubyte  * 4 ),
                 ("nmeaintv"   , ctypes.c_double * 2 ),
                 ("sep"        , ctypes.c_char   * 64 ),
                 ("prog"       , ctypes.c_char   * 64 )]
    def SetConstants(self):
        pass


class filopt_t (my_endian):
    """
filopt_t{        /* file options type */
    char satantp[MAXSTRPATH]; /* satellite antenna parameters file */
    char rcvantp[MAXSTRPATH]; /* receiver antenna parameters file */
    char stapos [MAXSTRPATH]; /* station positions file */
    char geoid  [MAXSTRPATH]; /* external geoid data file */
    char iono   [MAXSTRPATH]; /* ionosphere data file */
    char dcb    [MAXSTRPATH]; /* dcb data file */
    char eop    [MAXSTRPATH]; /* eop data file */
    char blq    [MAXSTRPATH]; /* ocean tide loading blq file */
    char tempdir[MAXSTRPATH]; /* ftp/http temporaly directory */
    char geexe  [MAXSTRPATH]; /* google earth exec file */
    char solstat[MAXSTRPATH]; /* solution statistics file */
    char trace  [MAXSTRPATH]; /* debug trace file */
} """
    _pack_ = 1

    _fields_ = [ ("satantp" , ctypes.c_char * 1024 ),
                 ("rcvantp" , ctypes.c_char * 1024 ),
                 ("stapos"  , ctypes.c_char * 1024 ),
                 ("geoid"   , ctypes.c_char * 1024 ),
                 ("iono"    , ctypes.c_char * 1024 ),
                 ("dcb"     , ctypes.c_char * 1024 ),
                 ("eop"     , ctypes.c_char * 1024 ),
                 ("blq"     , ctypes.c_char * 1024 ),
                 ("tempdir" , ctypes.c_char * 1024 ),
                 ("geexe"   , ctypes.c_char * 1024 ),
                 ("solstat" , ctypes.c_char * 1024 ),
                 ("trace"   , ctypes.c_char * 1024 )]
    def SetConstants(self):
        pass


class rnxopt_t (my_endian):
    """
rnxopt_t{        /* RINEX options type */
    gtime_t ts,te;      /* time start/end */
    double tint;        /* time interval (s) */
    double tunit;       /* time unit for multiple-session (s) */
    double rnxver;      /* RINEX version */
    int navsys;         /* navigation system */
    int obstype;        /* observation type */
    int freqtype;       /* frequency type */
    char mask[6][64];   /* code mask {GPS,GLO,GAL,QZS,SBS,CMP} */
    char staid [32];    /* station id for rinex file name */
    char prog  [32];    /* program */
    char runby [32];    /* run-by */
    char marker[64];    /* marker name */
    char markerno[32];  /* marker number */
    char markertype[32]; /* marker type (ver.3) */
    char name[2][32];   /* observer/agency */
    char rec [3][32];   /* receiver #/type/vers */
    char ant [3][32];   /* antenna #/type */
    double apppos[3];   /* approx position x/y/z */
    double antdel[3];   /* antenna delta h/e/n */
    char comment[MAXCOMMENT][64]; /* comments */
    char rcvopt[256];   /* receiver dependent options */
    unsigned char exsats[MAXSAT]; /* excluded satellites */
    int scanobs;        /* scan obs types */
    int outiono;        /* output iono correction */
    int outtime;        /* output time system correction */
    int outleaps;       /* output leap seconds */
    int autopos;        /* auto approx position */
    gtime_t tstart;     /* first obs time */
    gtime_t tend;       /* last obs time */
    gtime_t trtcm;      /* approx log start time for rtcm */
    char tobs[6][MAXOBSTYPE][4]; /* obs types {GPS,GLO,GAL,QZS,SBS,CMP} */
    int nobs[6];        /* number of obs types {GPS,GLO,GAL,QZS,SBS,CMP} */
} """
    _pack_ = 1

    _fields_ = [ ("ts"           , gtime_t ),
                 ("te"           , gtime_t ),
                 ("tint"         , ctypes.c_double ),
                 ("tunit"        , ctypes.c_double ),
                 ("rnxver"       , ctypes.c_double ),
                 ("navsys"       , ctypes.c_int ),
                 ("obstype"      , ctypes.c_int ),
                 ("freqtype"     , ctypes.c_int ),
                 ("mask"         , (ctypes.c_char  * 64) * 6 ),
                 ("staid"        , ctypes.c_char   * 32 ),
                 ("prog"         , ctypes.c_char   * 32 ),
                 ("runby"        , ctypes.c_char   * 32 ),
                 ("marker"       , ctypes.c_char   * 64 ),
                 ("markerno"     , ctypes.c_char   * 32 ),
                 ("markertype"   , ctypes.c_char   * 32 ),
                 ("name"         , (ctypes.c_char  * 32) * 2 ),
                 ("rec"          , (ctypes.c_char  * 32) * 3 ),
                 ("ant"          , (ctypes.c_char  * 32) * 3 ),
                 ("pad_7456_32"  , ctypes.c_ubyte  * 4 ),
                 ("apppos"       , ctypes.c_double * 3 ),
                 ("antdel"       , ctypes.c_double * 3 ),
                 ("comment"      , (ctypes.c_char  * 64) * 10 ),
                 ("rcvopt"       , ctypes.c_char   * 256 ),
                 ("exsats"       , ctypes.c_ubyte  * 55 ),
                 ("pad_15480_8"  , ctypes.c_ubyte ),
                 ("scanobs"      , ctypes.c_int ),
                 ("outiono"      , ctypes.c_int ),
                 ("outtime"      , ctypes.c_int ),
                 ("outleaps"     , ctypes.c_int ),
                 ("autopos"      , ctypes.c_int ),
                 ("pad_15648_32" , ctypes.c_ubyte  * 4 ),
                 ("tstart"       , gtime_t ),
                 ("tend"         , gtime_t ),
                 ("trtcm"        , gtime_t ),
                 ("tobs"         , ((ctypes.c_char * 4) * 64) * 6 ),
                 ("nobs"         , ctypes.c_int    * 6 )]
    def SetConstants(self):
        pass


class ssat_t (my_endian):
    """
ssat_t{        /* satellite status type */
    unsigned char sys;  /* navigation system */
    unsigned char vs;   /* valid satellite flag single */
    double azel[2];     /* azimuth/elevation angles {az,el} (rad) */
    double resp[NFREQ]; /* residuals of pseudorange (m) */
    double resc[NFREQ]; /* residuals of carrier-phase (m) */
    unsigned char vsat[NFREQ]; /* valid satellite flag */
    unsigned char snr [NFREQ]; /* signal strength (0.25 dBHz) */
    unsigned char fix [NFREQ]; /* ambiguity fix flag (1:fix,2:float,3:hold) */
    unsigned char slip[NFREQ]; /* cycle-slip flag */
    unsigned int lock [NFREQ]; /* lock counter of phase */
    unsigned int outc [NFREQ]; /* obs outage counter of phase */
    unsigned int slipc[NFREQ]; /* cycle-slip counter */
    unsigned int rejc [NFREQ]; /* reject counter */
    double  gf;         /* geometry-free phase L1-L2 (m) */
    double  gf2;        /* geometry-free phase L1-L5 (m) */
    double  phw;        /* phase windup (cycle) */
    gtime_t pt[2][NFREQ]; /* previous carrier-phase time */
    double  ph[2][NFREQ]; /* previous carrier-phase observable (cycle) */
} """
    _pack_ = 1

    _fields_ = [ ("sys"         , ctypes.c_ubyte ),
                 ("vs"          , ctypes.c_ubyte ),
                 ("pad_16_48"   , ctypes.c_ubyte   * 6 ),
                 ("azel"        , ctypes.c_double  * 2 ),
                 ("resp"        , ctypes.c_double  * 3 ),
                 ("resc"        , ctypes.c_double  * 3 ),
                 ("vsat"        , ctypes.c_ubyte   * 3 ),
                 ("snr"         , ctypes.c_ubyte   * 3 ),
                 ("fix"         , ctypes.c_ubyte   * 3 ),
                 ("slip"        , ctypes.c_ubyte   * 3 ),
                 ("lock"        , ctypes.c_uint    * 3 ),
                 ("outc"        , ctypes.c_uint    * 3 ),
                 ("slipc"       , ctypes.c_uint    * 3 ),
                 ("rejc"        , ctypes.c_uint    * 3 ),
                 ("pad_1056_32" , ctypes.c_ubyte   * 4 ),
                 ("gf"          , ctypes.c_double ),
                 ("gf2"         , ctypes.c_double ),
                 ("phw"         , ctypes.c_double ),
                 ("pt"          , (gtime_t         * 3) * 2 ),
                 ("ph"          , (ctypes.c_double * 3) * 2 )]
    def SetConstants(self):
        pass


class ambc_t (my_endian):
    """
ambc_t{        /* ambiguity control type */
    gtime_t epoch[4];   /* last epoch */
    int fixcnt;         /* fix counter */
    char flags[MAXSAT]; /* fix flags */
    double n[4];        /* number of epochs */
    double LC [4];      /* linear combination average */
    double LCv[4];      /* linear combination variance */
} """
    _pack_ = 1

    _fields_ = [ ("epoch"      , gtime_t         * 4 ),
                 ("fixcnt"     , ctypes.c_int ),
                 ("flags"      , ctypes.c_char   * 55 ),
                 ("pad_984_40" , ctypes.c_ubyte  * 5 ),
                 ("n"          , ctypes.c_double * 4 ),
                 ("LC"         , ctypes.c_double * 4 ),
                 ("LCv"        , ctypes.c_double * 4 )]
    def SetConstants(self):
        pass


class rtk_t (my_endian):
    """
rtk_t{        /* RTK control/result type */
    sol_t  sol;         /* RTK solution */
    double rb[6];       /* base position/velocity (ecef) (m|m/s) */
    int nx,na;          /* number of float states/fixed states */
    double tt;          /* time difference between current and previous (s) */
    double *x, *P;      /* float states and their covariance */
    double *xa,*Pa;     /* fixed states and their covariance */
    int nfix;           /* number of continuous fixes of ambiguity */
    ambc_t ambc[MAXSAT]; /* ambibuity control */
    ssat_t ssat[MAXSAT]; /* satellite status */
    int neb;            /* bytes in error message buffer */
    char errbuf[MAXERRMSG]; /* error message buffer */
    prcopt_t opt;       /* processing options */
} """
    _pack_ = 1

    _fields_ = [ ("sol"           , sol_t ),
                 ("rb"            , ctypes.c_double * 6 ),
                 ("nx"            , ctypes.c_int ),
                 ("na"            , ctypes.c_int ),
                 ("tt"            , ctypes.c_double ),
                 ("x"             , ctypes.POINTER(ctypes.c_double) ),
                 ("P"             , ctypes.POINTER(ctypes.c_double) ),
                 ("xa"            , ctypes.POINTER(ctypes.c_double) ),
                 ("Pa"            , ctypes.POINTER(ctypes.c_double) ),
                 ("nfix"          , ctypes.c_int ),
                 ("pad_2016_32"   , ctypes.c_ubyte  * 4 ),
                 ("ambc"          , ambc_t          * 55 ),
                 ("ssat"          , ssat_t          * 55 ),
                 ("neb"           , ctypes.c_int ),
                 ("errbuf"        , ctypes.c_char   * 4096 ),
                 ("pad_267168_32" , ctypes.c_ubyte  * 4 ),
                 ("opt"           , prcopt_t )]
    def SetConstants(self):
        pass


class raw_t (my_endian):
    """
raw_t{        /* receiver raw data control type */
    gtime_t time;       /* message time */
    gtime_t tobs;       /* observation data time */
    obs_t obs;          /* observation data */
    obs_t obuf;         /* observation data buffer */
    nav_t nav;          /* satellite ephemerides */
    sta_t sta;          /* station parameters */
    int ephsat;         /* sat number of update ephemeris (0:no satellite) */
    sbsmsg_t sbsmsg;    /* SBAS message */
    char msgtype[256];  /* last message type */
    unsigned char subfrm[MAXSAT][380];  /* subframe buffer */
    lexmsg_t lexmsg;    /* LEX message */
    double lockt[MAXSAT][NFREQ+NEXOBS]; /* lock time (s) */
    double icpp[MAXSAT],off[MAXSAT],icpc; /* carrier params for ss2 */
    double prCA[MAXSAT],dpCA[MAXSAT]; /* L1/CA pseudrange/doppler for javad */
    unsigned char halfc[MAXSAT][NFREQ+NEXOBS]; /* half-cycle add flag */
    char freqn[MAXOBS]; /* frequency number for javad */
    int nbyte;          /* number of bytes in message buffer */ 
    int len;            /* message length (bytes) */
    int iod;            /* issue of data */
    int tod;            /* time of day (ms) */
    int tbase;          /* time base (0:gpst,1:utc(usno),2:glonass,3:utc(su) */
    int flag;           /* general purpose flag */
    int outtype;        /* output message type */
    unsigned char buff[MAXRAWLEN]; /* message buffer */
    char opt[256];      /* receiver dependent options */
    double receive_time;/* RT17: Reiceve time of week for week rollover detection */
    unsigned int plen;  /* RT17: Total size of packet to be read */
    unsigned int pbyte; /* RT17: How many packet bytes have been read so far */
    unsigned int page;  /* RT17: Last page number */
    unsigned int reply; /* RT17: Current reply number */
    int week;           /* RT17: week number */
    unsigned char pbuff[255+4+2]; /* RT17: Packet buffer */
} """
    _pack_ = 1

    _fields_ = [ ("time"           , gtime_t ),
                 ("tobs"           , gtime_t ),
                 ("obs"            , obs_t ),
                 ("obuf"           , obs_t ),
                 ("nav"            , nav_t ),
                 ("sta"            , sta_t ),
                 ("ephsat"         , ctypes.c_int ),
                 ("sbsmsg"         , sbsmsg_t ),
                 ("msgtype"        , ctypes.c_char    * 256 ),
                 ("subfrm"         , (ctypes.c_ubyte  * 380) * 55 ),
                 ("lexmsg"         , lexmsg_t ),
                 ("pad_1452576_32" , ctypes.c_ubyte   * 4 ),
                 ("lockt"          , (ctypes.c_double * 3) * 55 ),
                 ("icpp"           , ctypes.c_double  * 55 ),
                 ("off"            , ctypes.c_double  * 55 ),
                 ("icpc"           , ctypes.c_double ),
                 ("prCA"           , ctypes.c_double  * 55 ),
                 ("dpCA"           , ctypes.c_double  * 55 ),
                 ("halfc"          , (ctypes.c_ubyte  * 3) * 55 ),
                 ("freqn"          , ctypes.c_char    * 64 ),
                 ("pad_1479144_24" , ctypes.c_ubyte   * 3 ),
                 ("nbyte"          , ctypes.c_int ),
                 ("len"            , ctypes.c_int ),
                 ("iod"            , ctypes.c_int ),
                 ("tod"            , ctypes.c_int ),
                 ("tbase"          , ctypes.c_int ),
                 ("flag"           , ctypes.c_int ),
                 ("outtype"        , ctypes.c_int ),
                 ("buff"           , ctypes.c_ubyte   * 4096 ),
                 ("opt"            , ctypes.c_char    * 256 ),
                 ("pad_1514208_32" , ctypes.c_ubyte   * 4 ),
                 ("receive_time"   , ctypes.c_double ),
                 ("plen"           , ctypes.c_uint ),
                 ("pbyte"          , ctypes.c_uint ),
                 ("page"           , ctypes.c_uint ),
                 ("reply"          , ctypes.c_uint ),
                 ("week"           , ctypes.c_int ),
                 ("pbuff"          , ctypes.c_ubyte   * 261 ),
                 ("pad_1516552_56" , ctypes.c_ubyte   * 7 )]
    def SetConstants(self):
        pass


class _opaque_pthread_mutex_t (my_endian):
    """
_opaque_pthread_mutex_t { long __sig; char __opaque[__PTHREAD_MUTEX_SIZE__]; }"""
    _pack_ = 1

    _fields_ = [ ("__sig"    , ctypes.c_int64 ),
                 ("__opaque" , ctypes.c_char * 56 )]
    def SetConstants(self):
        pass


class stream_t (my_endian):
    """
stream_t{        /* stream type */
    int type;           /* type (STR_???) */
    int mode;           /* mode (STR_MODE_?) */
    int state;          /* state (-1:error,0:close,1:open) */
    unsigned int inb,inr;   /* input bytes/rate */
    unsigned int outb,outr; /* output bytes/rate */
    unsigned int tick,tact; /* tick/active tick */
    unsigned int inbt,outbt; /* input/output bytes at tick */
    lock_t lock;        /* lock flag */
    void *port;         /* type dependent port control struct */
    char path[MAXSTRPATH]; /* stream path */
    char msg [MAXSTRMSG];  /* stream message */
} """
    _pack_ = 1

    _fields_ = [ ("type"       , ctypes.c_int ),
                 ("mode"       , ctypes.c_int ),
                 ("state"      , ctypes.c_int ),
                 ("inb"        , ctypes.c_uint ),
                 ("inr"        , ctypes.c_uint ),
                 ("outb"       , ctypes.c_uint ),
                 ("outr"       , ctypes.c_uint ),
                 ("tick"       , ctypes.c_uint ),
                 ("tact"       , ctypes.c_uint ),
                 ("inbt"       , ctypes.c_uint ),
                 ("outbt"      , ctypes.c_uint ),
                 ("pad_352_32" , ctypes.c_ubyte * 4 ),
                 ("lock"       , _opaque_pthread_mutex_t ),
                 ("port"       , ctypes.POINTER(None) ),
                 ("path"       , ctypes.c_char  * 1024 ),
                 ("msg"        , ctypes.c_char  * 1024 )]
    def SetConstants(self):
        pass


class strconv_t (my_endian):
    """
strconv_t{        /* stream converter type */
    int itype,otype;    /* input and output stream type */
    int nmsg;           /* number of output messages */
    int msgs[32];       /* output message types */
    double tint[32];    /* output message intervals (s) */
    unsigned int tick[32]; /* cycle tick of output message */
    int ephsat[32];     /* satellites of output ephemeris */
    int stasel;         /* station info selection (0:remote,1:local) */
    rtcm_t rtcm;        /* rtcm input data buffer */
    raw_t raw;          /* raw  input data buffer */
    rtcm_t out;         /* rtcm output data buffer */
} """
    _pack_ = 1

    _fields_ = [ ("itype"       , ctypes.c_int ),
                 ("otype"       , ctypes.c_int ),
                 ("nmsg"        , ctypes.c_int ),
                 ("msgs"        , ctypes.c_int    * 32 ),
                 ("pad_1120_32" , ctypes.c_ubyte  * 4 ),
                 ("tint"        , ctypes.c_double * 32 ),
                 ("tick"        , ctypes.c_uint   * 32 ),
                 ("ephsat"      , ctypes.c_int    * 32 ),
                 ("stasel"      , ctypes.c_int ),
                 ("pad_5280_32" , ctypes.c_ubyte  * 4 ),
                 ("rtcm"        , rtcm_t ),
                 ("raw"         , raw_t ),
                 ("out"         , rtcm_t )]
    def SetConstants(self):
        pass


class strsvr_t (my_endian):
    """
strsvr_t{        /* stream server type */
    int state;          /* server state (0:stop,1:running) */
    int cycle;          /* server cycle (ms) */
    int buffsize;       /* input/monitor buffer size (bytes) */
    int nmeacycle;      /* NMEA request cycle (ms) (0:no) */
    int nstr;           /* number of streams (1 input + (nstr-1) outputs */
    int npb;            /* data length in peek buffer (bytes) */
    double nmeapos[3];  /* NMEA request position (ecef) (m) */
    unsigned char *buff; /* input buffers */
    unsigned char *pbuf; /* peek buffer */
    unsigned int tick;  /* start tick */
    stream_t stream[16]; /* input/output streams */
    strconv_t *conv[16]; /* stream converter */
    thread_t thread;    /* server thread */
    lock_t lock;        /* lock flag */
} """
    _pack_ = 1

    _fields_ = [ ("state"      , ctypes.c_int ),
                 ("cycle"      , ctypes.c_int ),
                 ("buffsize"   , ctypes.c_int ),
                 ("nmeacycle"  , ctypes.c_int ),
                 ("nstr"       , ctypes.c_int ),
                 ("npb"        , ctypes.c_int ),
                 ("nmeapos"    , ctypes.c_double * 3 ),
                 ("buff"       , ctypes.POINTER(ctypes.c_uint64) ),
                 ("pbuf"       , ctypes.POINTER(ctypes.c_uint64) ),
                 ("tick"       , ctypes.c_uint ),
                 ("pad_544_32" , ctypes.c_ubyte  * 4 ),
                 ("stream"     , stream_t        * 16 ),
                 ("conv"       , ctypes.c_void_p * 16 ),
                 ("thread"     , ctypes.c_void_p ),
                 ("lock"       , _opaque_pthread_mutex_t )]
    def SetConstants(self):
        pass


class rtksvr_t (my_endian):
    """
rtksvr_t{        /* RTK server type */
    int state;          /* server state (0:stop,1:running) */
    int cycle;          /* processing cycle (ms) */
    int nmeacycle;      /* NMEA request cycle (ms) (0:no req) */
    int nmeareq;        /* NMEA request (0:no,1:nmeapos,2:single sol) */
    double nmeapos[3];  /* NMEA request position (ecef) (m) */
    int buffsize;       /* input buffer size (bytes) */
    int format[3];      /* input format {rov,base,corr} */
    solopt_t solopt[2]; /* output solution options {sol1,sol2} */
    int navsel;         /* ephemeris select (0:all,1:rover,2:base,3:corr) */
    int nsbs;           /* number of sbas message */
    int nsol;           /* number of solution buffer */
    rtk_t rtk;          /* RTK control/result struct */
    int nb [3];         /* bytes in input buffers {rov,base} */
    int nsb[2];         /* bytes in soulution buffers */
    int npb[3];         /* bytes in input peek buffers */
    unsigned char *buff[3]; /* input buffers {rov,base,corr} */
    unsigned char *sbuf[2]; /* output buffers {sol1,sol2} */
    unsigned char *pbuf[3]; /* peek buffers {rov,base,corr} */
    sol_t solbuf[MAXSOLBUF]; /* solution buffer */
    unsigned int nmsg[3][10]; /* input message counts */
    raw_t  raw [3];     /* receiver raw control {rov,base,corr} */
    rtcm_t rtcm[3];     /* RTCM control {rov,base,corr} */
    gtime_t ftime[3];   /* download time {rov,base,corr} */
    char files[3][MAXSTRPATH]; /* download paths {rov,base,corr} */
    obs_t obs[3][MAXOBSBUF]; /* observation data {rov,base,corr} */
    nav_t nav;          /* navigation data */
    sbsmsg_t sbsmsg[MAXSBSMSG]; /* SBAS message buffer */
    stream_t stream[8]; /* streams {rov,base,corr,sol1,sol2,logr,logb,logc} */
    stream_t *moni;     /* monitor stream */
    unsigned int tick;  /* start tick */
    thread_t thread;    /* server thread */
    int cputime;        /* CPU time (ms) for a processing cycle */
    int prcout;         /* missing observation data count */
    lock_t lock;        /* lock flag */
} """
    _pack_ = 1

    _fields_ = [ ("state"           , ctypes.c_int ),
                 ("cycle"           , ctypes.c_int ),
                 ("nmeacycle"       , ctypes.c_int ),
                 ("nmeareq"         , ctypes.c_int ),
                 ("nmeapos"         , ctypes.c_double * 3 ),
                 ("buffsize"        , ctypes.c_int ),
                 ("format"          , ctypes.c_int    * 3 ),
                 ("solopt"          , solopt_t        * 2 ),
                 ("navsel"          , ctypes.c_int ),
                 ("nsbs"            , ctypes.c_int ),
                 ("nsol"            , ctypes.c_int ),
                 ("pad_3744_32"     , ctypes.c_ubyte  * 4 ),
                 ("rtk"             , rtk_t ),
                 ("nb"              , ctypes.c_int    * 3 ),
                 ("nsb"             , ctypes.c_int    * 2 ),
                 ("npb"             , ctypes.c_int    * 3 ),
                 ("buff"            , ctypes.c_void_p * 3 ),
                 ("sbuf"            , ctypes.c_void_p * 2 ),
                 ("pbuf"            , ctypes.c_void_p * 3 ),
                 ("solbuf"          , sol_t           * 256 ),
                 ("nmsg"            , (ctypes.c_uint  * 10) * 3 ),
                 ("raw"             , raw_t           * 3 ),
                 ("rtcm"            , rtcm_t          * 3 ),
                 ("ftime"           , gtime_t         * 3 ),
                 ("files"           , (ctypes.c_char  * 1024) * 3 ),
                 ("obs"             , (obs_t          * 128) * 3 ),
                 ("nav"             , nav_t ),
                 ("sbsmsg"          , sbsmsg_t        * 32 ),
                 ("stream"          , stream_t        * 8 ),
                 ("moni"            , ctypes.POINTER(stream_t) ),
                 ("tick"            , ctypes.c_uint ),
                 ("pad_11287008_32" , ctypes.c_ubyte  * 4 ),
                 ("thread"          , ctypes.c_void_p ),
                 ("cputime"         , ctypes.c_int ),
                 ("prcout"          , ctypes.c_int ),
                 ("lock"            , _opaque_pthread_mutex_t )]
    def SetConstants(self):
        pass



rtklib.satno.argtypes = [ctypes.c_int,ctypes.c_int]
rtklib.satno.restype = ctypes.c_int
def satno(sys,prn):
  """
satno   (int sys, int prn)"""

  result = rtklib.satno(sys,prn)


  return result

rtklib.satsys.argtypes = [ctypes.c_int,ctypes.POINTER(ctypes.c_int)]
rtklib.satsys.restype = ctypes.c_int
def satsys(sat,prn):
  """
satsys  (int sat, int *prn)"""

  result = rtklib.satsys(sat,prn)


  return result

rtklib.satid2no.argtypes = [ctypes.POINTER(ctypes.c_char)]
rtklib.satid2no.restype = ctypes.c_int
def satid2no(id):
  """
satid2no(const char *id)"""

  result = rtklib.satid2no(id)


  return result

rtklib.satno2id.argtypes = [ctypes.c_int,ctypes.POINTER(ctypes.c_char)]
rtklib.satno2id.restype = None
def satno2id(sat,id):
  """
satno2id(int sat, char *id)"""

  result = rtklib.satno2id(sat,id)


  return result

rtklib.obs2code.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.POINTER(ctypes.c_int)]
rtklib.obs2code.restype = ctypes.c_ubyte
def obs2code(obs,freq):
  """
obs2code(const char *obs, int *freq)"""

  result = rtklib.obs2code(obs,freq)


  return result

rtklib.code2obs.argtypes = [ctypes.c_ubyte,ctypes.POINTER(ctypes.c_int)]
rtklib.code2obs.restype = ctypes.POINTER(ctypes.c_char)
def code2obs(code,freq):
  """
code2obs(unsigned char code, int *freq)"""

  result = rtklib.code2obs(code,freq)


  return result

rtklib.satexclude.argtypes = [ctypes.c_int,ctypes.c_int,ctypes.POINTER(prcopt_t)]
rtklib.satexclude.restype = ctypes.c_int
def satexclude(sat,svh,opt):
  """
satexclude(int sat, int svh, const prcopt_t *opt)"""

  if(type(opt) == prcopt_t):
    opt = ctypes.byref(opt)

  result = rtklib.satexclude(sat,svh,opt)


  return result

rtklib.testsnr.argtypes = [ctypes.c_int,ctypes.c_int,ctypes.c_double,ctypes.c_double,ctypes.POINTER(snrmask_t)]
rtklib.testsnr.restype = ctypes.c_int
def testsnr(base,freq,el,snr,mask):
  """
testsnr(int base, int freq, double el, double snr,
                    const snrmask_t *mask)"""

  if(type(mask) == snrmask_t):
    mask = ctypes.byref(mask)

  result = rtklib.testsnr(base,freq,el,snr,mask)


  return result

rtklib.setcodepri.argtypes = [ctypes.c_int,ctypes.c_int,ctypes.POINTER(ctypes.c_char)]
rtklib.setcodepri.restype = None
def setcodepri(sys,freq,pri):
  """
setcodepri(int sys, int freq, const char *pri)"""

  result = rtklib.setcodepri(sys,freq,pri)


  return result

rtklib.getcodepri.argtypes = [ctypes.c_int,ctypes.c_ubyte,ctypes.POINTER(ctypes.c_char)]
rtklib.getcodepri.restype = ctypes.c_int
def getcodepri(sys,code,opt):
  """
getcodepri(int sys, unsigned char code, const char *opt)"""

  result = rtklib.getcodepri(sys,code,opt)


  return result

rtklib.mat.argtypes = [ctypes.c_int,ctypes.c_int]
rtklib.mat.restype = ctypes.POINTER(ctypes.c_double)
def mat(n,m):
  """
mat  (int n, int m)"""

  result = rtklib.mat(n,m)


  return result

rtklib.imat.argtypes = [ctypes.c_int,ctypes.c_int]
rtklib.imat.restype = ctypes.POINTER(ctypes.c_int)
def imat(n,m):
  """
imat (int n, int m)"""

  result = rtklib.imat(n,m)


  return result

rtklib.zeros.argtypes = [ctypes.c_int,ctypes.c_int]
rtklib.zeros.restype = ctypes.POINTER(ctypes.c_double)
def zeros(n,m):
  """
zeros(int n, int m)"""

  result = rtklib.zeros(n,m)


  return result

rtklib.eye.argtypes = [ctypes.c_int]
rtklib.eye.restype = ctypes.POINTER(ctypes.c_double)
def eye(n):
  """
eye  (int n)"""

  result = rtklib.eye(n)


  return result

rtklib.dot.argtypes = [ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.c_int]
rtklib.dot.restype = ctypes.c_double
def dot(a,b,n):
  """
dot (const double *a, const double *b, int n)"""

  result = rtklib.dot(a,b,n)


  return result

rtklib.norm.argtypes = [ctypes.POINTER(ctypes.c_double),ctypes.c_int]
rtklib.norm.restype = ctypes.c_double
def norm(a,n):
  """
norm(const double *a, int n)"""

  result = rtklib.norm(a,n)


  return result

rtklib.cross3.argtypes = [ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
rtklib.cross3.restype = None
def cross3(a,b,c):
  """
cross3(const double *a, const double *b, double *c)"""

  result = rtklib.cross3(a,b,c)


  return result

rtklib.normv3.argtypes = [ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
rtklib.normv3.restype = ctypes.c_int
def normv3(a,b):
  """
normv3(const double *a, double *b)"""

  result = rtklib.normv3(a,b)


  return result

rtklib.matcpy.argtypes = [ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.c_int,ctypes.c_int]
rtklib.matcpy.restype = None
def matcpy(A,B,n,m):
  """
matcpy(double *A, const double *B, int n, int m)"""

  result = rtklib.matcpy(A,B,n,m)


  return result

rtklib.matmul.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_double,ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.c_double,ctypes.POINTER(ctypes.c_double)]
rtklib.matmul.restype = None
def matmul(tr,n,k,m,alpha,A,B,beta,C):
  """
matmul(const char *tr, int n, int k, int m, double alpha,
                   const double *A, const double *B, double beta, double *C)"""

  result = rtklib.matmul(tr,n,k,m,alpha,A,B,beta,C)


  return result

rtklib.matinv.argtypes = [ctypes.POINTER(ctypes.c_double),ctypes.c_int]
rtklib.matinv.restype = ctypes.c_int
def matinv(A,n):
  """
matinv(double *A, int n)"""

  result = rtklib.matinv(A,n)


  return result

rtklib.solve.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.c_int,ctypes.c_int,ctypes.POINTER(ctypes.c_double)]
rtklib.solve.restype = ctypes.c_int
def solve(tr,A,Y,n,m,X):
  """
solve (const char *tr, const double *A, const double *Y, int n,
                   int m, double *X)"""

  result = rtklib.solve(tr,A,Y,n,m,X)


  return result

rtklib.lsq.argtypes = [ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.c_int,ctypes.c_int,ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
rtklib.lsq.restype = ctypes.c_int
def lsq(A,y,n,m,x,Q):
  """
lsq   (const double *A, const double *y, int n, int m, double *x,
                   double *Q)"""

  result = rtklib.lsq(A,y,n,m,x,Q)


  return result

rtklib.filter.argtypes = [ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.c_int,ctypes.c_int]
rtklib.filter.restype = ctypes.c_int
def filter(x,P,H,v,R,n,m):
  """
filter(double *x, double *P, const double *H, const double *v,
                   const double *R, int n, int m)"""

  result = rtklib.filter(x,P,H,v,R,n,m)


  return result

rtklib.smoother.argtypes = [ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.c_int,ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
rtklib.smoother.restype = ctypes.c_int
def smoother(xf,Qf,xb,Qb,n,xs,Qs):
  """
smoother(const double *xf, const double *Qf, const double *xb,
                     const double *Qb, int n, double *xs, double *Qs)"""

  result = rtklib.smoother(xf,Qf,xb,Qb,n,xs,Qs)


  return result

rtklib.matprint.argtypes = [ctypes.POINTER(ctypes.c_double),ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int]
rtklib.matprint.restype = None
def matprint(A,n,m,p,q):
  """
matprint (const double *A, int n, int m, int p, int q)"""

  result = rtklib.matprint(A,n,m,p,q)


  return result

rtklib.matfprint.argtypes = [ctypes.POINTER(ctypes.c_double),ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.POINTER(None)]
rtklib.matfprint.restype = None
def matfprint(A,n,m,p,q,fp):
  """
matfprint(const double *A, int n, int m, int p, int q, FILE *fp)"""

  result = rtklib.matfprint(A,n,m,p,q,fp)


  return result

rtklib.openfile.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.POINTER(ctypes.c_char)]
rtklib.openfile.restype = ctypes.POINTER(None)
def openfile(filename,mode):
  """/*!
* @brief FILE* pointer for python interface
* @param filename
*   @brief Filename of the file to be opened.
* @param mode
*   @brief Flags for opening the file, ie "w", "a", "r"
* @return
*    @brief File pointer
*/
openfile(const char* filename, const char * mode )"""

  result = rtklib.openfile(filename,mode)


  return result

rtklib.closefile.argtypes = [ctypes.POINTER(None)]
rtklib.closefile.restype = ctypes.c_int
def closefile(file):
  """/*!
* @brief FILE* pointer for python interface
* @param filename
*   @brief File pointer of the file to be closed
* @return
*    @brief status code, 0=success, +num=warnings,-num=errors
*    @status
*/
closefile(FILE*file)"""

  result = rtklib.closefile(file)



  if (result < 0):
    er = 'rtklib:neg_{val}'.format(val=abs(result))
    raise Exception(er)
  elif(result > 0):
    er = 'rtklib:pos_{val}'.format(val=abs(result))
    warnings.warn(er)
  return result

rtklib.str2num.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.c_int,ctypes.c_int]
rtklib.str2num.restype = ctypes.c_double
def str2num(s,i,n):
  """
str2num(const char *s, int i, int n)"""

  result = rtklib.str2num(s,i,n)


  return result

rtklib.str2time.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.c_int,ctypes.c_int,ctypes.POINTER(gtime_t)]
rtklib.str2time.restype = ctypes.c_int
def str2time(s,i,n,t):
  """
str2time(const char *s, int i, int n, gtime_t *t)"""

  if(type(t) == gtime_t):
    t = ctypes.byref(t)

  result = rtklib.str2time(s,i,n,t)


  return result

rtklib.time2str.argtypes = [gtime_t,ctypes.POINTER(ctypes.c_char),ctypes.c_int]
rtklib.time2str.restype = None
def time2str(t,str,n):
  """
time2str(gtime_t t, char *str, int n)"""

  result = rtklib.time2str(t,str,n)


  return result

rtklib.epoch2time.argtypes = [ctypes.POINTER(ctypes.c_double)]
rtklib.epoch2time.restype = gtime_t
def epoch2time(ep):
  """
epoch2time(const double *ep)"""

  result = rtklib.epoch2time(ep)


  return result

rtklib.time2epoch.argtypes = [gtime_t,ctypes.POINTER(ctypes.c_double)]
rtklib.time2epoch.restype = None
def time2epoch(t,ep):
  """
time2epoch(gtime_t t, double *ep)"""

  result = rtklib.time2epoch(t,ep)


  return result

rtklib.gpst2time.argtypes = [ctypes.c_int,ctypes.c_double]
rtklib.gpst2time.restype = gtime_t
def gpst2time(week,sec):
  """
gpst2time(int week, double sec)"""

  result = rtklib.gpst2time(week,sec)


  return result

rtklib.time2gpst.argtypes = [gtime_t,ctypes.POINTER(ctypes.c_int)]
rtklib.time2gpst.restype = ctypes.c_double
def time2gpst(t,week):
  """
time2gpst(gtime_t t, int *week)"""

  result = rtklib.time2gpst(t,week)


  return result

rtklib.gst2time.argtypes = [ctypes.c_int,ctypes.c_double]
rtklib.gst2time.restype = gtime_t
def gst2time(week,sec):
  """
gst2time(int week, double sec)"""

  result = rtklib.gst2time(week,sec)


  return result

rtklib.time2gst.argtypes = [gtime_t,ctypes.POINTER(ctypes.c_int)]
rtklib.time2gst.restype = ctypes.c_double
def time2gst(t,week):
  """
time2gst(gtime_t t, int *week)"""

  result = rtklib.time2gst(t,week)


  return result

rtklib.bdt2time.argtypes = [ctypes.c_int,ctypes.c_double]
rtklib.bdt2time.restype = gtime_t
def bdt2time(week,sec):
  """
bdt2time(int week, double sec)"""

  result = rtklib.bdt2time(week,sec)


  return result

rtklib.time2bdt.argtypes = [gtime_t,ctypes.POINTER(ctypes.c_int)]
rtklib.time2bdt.restype = ctypes.c_double
def time2bdt(t,week):
  """
time2bdt(gtime_t t, int *week)"""

  result = rtklib.time2bdt(t,week)


  return result

rtklib.time_str.argtypes = [gtime_t,ctypes.c_int]
rtklib.time_str.restype = ctypes.POINTER(ctypes.c_char)
def time_str(t,n):
  """
time_str(gtime_t t, int n)"""

  result = rtklib.time_str(t,n)


  return result

rtklib.timeadd.argtypes = [gtime_t,ctypes.c_double]
rtklib.timeadd.restype = gtime_t
def timeadd(t,sec):
  """
timeadd  (gtime_t t, double sec)"""

  result = rtklib.timeadd(t,sec)


  return result

rtklib.timediff.argtypes = [gtime_t,gtime_t]
rtklib.timediff.restype = ctypes.c_double
def timediff(t1,t2):
  """
timediff (gtime_t t1, gtime_t t2)"""

  result = rtklib.timediff(t1,t2)


  return result

rtklib.gpst2utc.argtypes = [gtime_t]
rtklib.gpst2utc.restype = gtime_t
def gpst2utc(t):
  """
gpst2utc (gtime_t t)"""

  result = rtklib.gpst2utc(t)


  return result

rtklib.utc2gpst.argtypes = [gtime_t]
rtklib.utc2gpst.restype = gtime_t
def utc2gpst(t):
  """
utc2gpst (gtime_t t)"""

  result = rtklib.utc2gpst(t)


  return result

rtklib.gpst2bdt.argtypes = [gtime_t]
rtklib.gpst2bdt.restype = gtime_t
def gpst2bdt(t):
  """
gpst2bdt (gtime_t t)"""

  result = rtklib.gpst2bdt(t)


  return result

rtklib.bdt2gpst.argtypes = [gtime_t]
rtklib.bdt2gpst.restype = gtime_t
def bdt2gpst(t):
  """
bdt2gpst (gtime_t t)"""

  result = rtklib.bdt2gpst(t)


  return result

rtklib.timeget.argtypes = []
rtklib.timeget.restype = gtime_t
def timeget():
  """
timeget  (void)"""

  result = rtklib.timeget()


  return result

rtklib.timeset.argtypes = [gtime_t]
rtklib.timeset.restype = None
def timeset(t):
  """
timeset  (gtime_t t)"""

  result = rtklib.timeset(t)


  return result

rtklib.time2doy.argtypes = [gtime_t]
rtklib.time2doy.restype = ctypes.c_double
def time2doy(t):
  """
time2doy (gtime_t t)"""

  result = rtklib.time2doy(t)


  return result

rtklib.utc2gmst.argtypes = [gtime_t,ctypes.c_double]
rtklib.utc2gmst.restype = ctypes.c_double
def utc2gmst(t,ut1_utc):
  """
utc2gmst (gtime_t t, double ut1_utc)"""

  result = rtklib.utc2gmst(t,ut1_utc)


  return result

rtklib.adjgpsweek.argtypes = [ctypes.c_int]
rtklib.adjgpsweek.restype = ctypes.c_int
def adjgpsweek(week):
  """
adjgpsweek(int week)"""

  result = rtklib.adjgpsweek(week)


  return result

rtklib.tickget.argtypes = []
rtklib.tickget.restype = ctypes.c_uint
def tickget():
  """
tickget(void)"""

  result = rtklib.tickget()


  return result

rtklib.sleepms.argtypes = [ctypes.c_int]
rtklib.sleepms.restype = None
def sleepms(ms):
  """
sleepms(int ms)"""

  result = rtklib.sleepms(ms)


  return result

rtklib.reppath.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.POINTER(ctypes.c_char),gtime_t,ctypes.POINTER(ctypes.c_char),ctypes.POINTER(ctypes.c_char)]
rtklib.reppath.restype = ctypes.c_int
def reppath(path,rpath,time,rov,base):
  """
reppath(const char *path, char *rpath, gtime_t time, const char *rov,
                   const char *base)"""

  result = rtklib.reppath(path,rpath,time,rov,base)


  return result

rtklib.ecef2pos.argtypes = [ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
rtklib.ecef2pos.restype = None
def ecef2pos(r,pos):
  """
ecef2pos(const double *r, double *pos)"""

  result = rtklib.ecef2pos(r,pos)


  return result

rtklib.pos2ecef.argtypes = [ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
rtklib.pos2ecef.restype = None
def pos2ecef(pos,r):
  """
pos2ecef(const double *pos, double *r)"""

  result = rtklib.pos2ecef(pos,r)


  return result

rtklib.ecef2enu.argtypes = [ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
rtklib.ecef2enu.restype = None
def ecef2enu(pos,r,e):
  """
ecef2enu(const double *pos, const double *r, double *e)"""

  result = rtklib.ecef2enu(pos,r,e)


  return result

rtklib.enu2ecef.argtypes = [ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
rtklib.enu2ecef.restype = None
def enu2ecef(pos,e,r):
  """
enu2ecef(const double *pos, const double *e, double *r)"""

  result = rtklib.enu2ecef(pos,e,r)


  return result

rtklib.covenu.argtypes = [ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
rtklib.covenu.restype = None
def covenu(pos,P,Q):
  """
covenu  (const double *pos, const double *P, double *Q)"""

  result = rtklib.covenu(pos,P,Q)


  return result

rtklib.covecef.argtypes = [ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
rtklib.covecef.restype = None
def covecef(pos,Q,P):
  """
covecef (const double *pos, const double *Q, double *P)"""

  result = rtklib.covecef(pos,Q,P)


  return result

rtklib.xyz2enu.argtypes = [ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
rtklib.xyz2enu.restype = None
def xyz2enu(pos,E):
  """
xyz2enu (const double *pos, double *E)"""

  result = rtklib.xyz2enu(pos,E)


  return result

rtklib.eci2ecef.argtypes = [gtime_t,ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
rtklib.eci2ecef.restype = None
def eci2ecef(tutc,erpv,U,gmst):
  """
eci2ecef(gtime_t tutc, const double *erpv, double *U, double *gmst)"""

  result = rtklib.eci2ecef(tutc,erpv,U,gmst)


  return result

rtklib.deg2dms.argtypes = [ctypes.c_double,ctypes.POINTER(ctypes.c_double)]
rtklib.deg2dms.restype = None
def deg2dms(deg,dms):
  """
deg2dms (double deg, double *dms)"""

  result = rtklib.deg2dms(deg,dms)


  return result

rtklib.dms2deg.argtypes = [ctypes.POINTER(ctypes.c_double)]
rtklib.dms2deg.restype = ctypes.c_double
def dms2deg(dms):
  """
dms2deg(const double *dms)"""

  result = rtklib.dms2deg(dms)


  return result

rtklib.readpos.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.POINTER(ctypes.c_char),ctypes.POINTER(ctypes.c_double)]
rtklib.readpos.restype = None
def readpos(file,rcv,pos):
  """
readpos(const char *file, const char *rcv, double *pos)"""

  result = rtklib.readpos(file,rcv,pos)


  return result

rtklib.sortobs.argtypes = [ctypes.POINTER(obs_t)]
rtklib.sortobs.restype = ctypes.c_int
def sortobs(obs):
  """
sortobs(obs_t *obs)"""

  if(type(obs) == obs_t):
    obs = ctypes.byref(obs)

  result = rtklib.sortobs(obs)


  return result

rtklib.uniqnav.argtypes = [ctypes.POINTER(nav_t)]
rtklib.uniqnav.restype = None
def uniqnav(nav):
  """
uniqnav(nav_t *nav)"""

  if(type(nav) == nav_t):
    nav = ctypes.byref(nav)

  result = rtklib.uniqnav(nav)


  return result

rtklib.screent.argtypes = [gtime_t,gtime_t,gtime_t,ctypes.c_double]
rtklib.screent.restype = ctypes.c_int
def screent(time,ts,te,tint):
  """
screent(gtime_t time, gtime_t ts, gtime_t te, double tint)"""

  result = rtklib.screent(time,ts,te,tint)


  return result

rtklib.readnav.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.POINTER(nav_t)]
rtklib.readnav.restype = ctypes.c_int
def readnav(file,nav):
  """
readnav(const char *file, nav_t *nav)"""

  if(type(nav) == nav_t):
    nav = ctypes.byref(nav)

  result = rtklib.readnav(file,nav)


  return result

rtklib.savenav.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.POINTER(nav_t)]
rtklib.savenav.restype = ctypes.c_int
def savenav(file,nav):
  """
savenav(const char *file, const nav_t *nav)"""

  if(type(nav) == nav_t):
    nav = ctypes.byref(nav)

  result = rtklib.savenav(file,nav)


  return result

rtklib.freeobs.argtypes = [ctypes.POINTER(obs_t)]
rtklib.freeobs.restype = None
def freeobs(obs):
  """
freeobs(obs_t *obs)"""

  if(type(obs) == obs_t):
    obs = ctypes.byref(obs)

  result = rtklib.freeobs(obs)


  return result

rtklib.freenav.argtypes = [ctypes.POINTER(nav_t),ctypes.c_int]
rtklib.freenav.restype = None
def freenav(nav,opt):
  """
freenav(nav_t *nav, int opt)"""

  if(type(nav) == nav_t):
    nav = ctypes.byref(nav)

  result = rtklib.freenav(nav,opt)


  return result

rtklib.readblq.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.POINTER(ctypes.c_char),ctypes.POINTER(ctypes.c_double)]
rtklib.readblq.restype = ctypes.c_int
def readblq(file,sta,odisp):
  """
readblq(const char *file, const char *sta, double *odisp)"""

  result = rtklib.readblq(file,sta,odisp)


  return result

rtklib.readerp.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.POINTER(erp_t)]
rtklib.readerp.restype = ctypes.c_int
def readerp(file,erp):
  """
readerp(const char *file, erp_t *erp)"""

  if(type(erp) == erp_t):
    erp = ctypes.byref(erp)

  result = rtklib.readerp(file,erp)


  return result

rtklib.geterp.argtypes = [ctypes.POINTER(erp_t),gtime_t,ctypes.POINTER(ctypes.c_double)]
rtklib.geterp.restype = ctypes.c_int
def geterp(erp,time,val):
  """
geterp (const erp_t *erp, gtime_t time, double *val)"""

  if(type(erp) == erp_t):
    erp = ctypes.byref(erp)

  result = rtklib.geterp(erp,time,val)


  return result

rtklib.traceopen.argtypes = [ctypes.POINTER(ctypes.c_char)]
rtklib.traceopen.restype = None
def traceopen(file):
  """
traceopen(const char *file)"""

  result = rtklib.traceopen(file)


  return result

rtklib.traceclose.argtypes = []
rtklib.traceclose.restype = None
def traceclose():
  """
traceclose(void)"""

  result = rtklib.traceclose()


  return result

rtklib.tracelevel.argtypes = [ctypes.c_int]
rtklib.tracelevel.restype = None
def tracelevel(level):
  """
tracelevel(int level)"""

  result = rtklib.tracelevel(level)


  return result

rtklib.trace.argtypes = [ctypes.c_int,ctypes.POINTER(ctypes.c_char)]
rtklib.trace.restype = None
def trace(level,format):
  """
trace    (int level, const char *format, ...)"""

  result = rtklib.trace(level,format)


  return result

rtklib.tracet.argtypes = [ctypes.c_int,ctypes.POINTER(ctypes.c_char)]
rtklib.tracet.restype = None
def tracet(level,format):
  """
tracet   (int level, const char *format, ...)"""

  result = rtklib.tracet(level,format)


  return result

rtklib.tracemat.argtypes = [ctypes.c_int,ctypes.POINTER(ctypes.c_double),ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int]
rtklib.tracemat.restype = None
def tracemat(level,A,n,m,p,q):
  """
tracemat (int level, const double *A, int n, int m, int p, int q)"""

  result = rtklib.tracemat(level,A,n,m,p,q)


  return result

rtklib.traceobs.argtypes = [ctypes.c_int,ctypes.POINTER(obsd_t),ctypes.c_int]
rtklib.traceobs.restype = None
def traceobs(level,obs,n):
  """
traceobs (int level, const obsd_t *obs, int n)"""

  if(type(obs) == obsd_t):
    obs = ctypes.byref(obs)

  result = rtklib.traceobs(level,obs,n)


  return result

rtklib.tracenav.argtypes = [ctypes.c_int,ctypes.POINTER(nav_t)]
rtklib.tracenav.restype = None
def tracenav(level,nav):
  """
tracenav (int level, const nav_t *nav)"""

  if(type(nav) == nav_t):
    nav = ctypes.byref(nav)

  result = rtklib.tracenav(level,nav)


  return result

rtklib.tracegnav.argtypes = [ctypes.c_int,ctypes.POINTER(nav_t)]
rtklib.tracegnav.restype = None
def tracegnav(level,nav):
  """
tracegnav(int level, const nav_t *nav)"""

  if(type(nav) == nav_t):
    nav = ctypes.byref(nav)

  result = rtklib.tracegnav(level,nav)


  return result

rtklib.tracehnav.argtypes = [ctypes.c_int,ctypes.POINTER(nav_t)]
rtklib.tracehnav.restype = None
def tracehnav(level,nav):
  """
tracehnav(int level, const nav_t *nav)"""

  if(type(nav) == nav_t):
    nav = ctypes.byref(nav)

  result = rtklib.tracehnav(level,nav)


  return result

rtklib.tracepeph.argtypes = [ctypes.c_int,ctypes.POINTER(nav_t)]
rtklib.tracepeph.restype = None
def tracepeph(level,nav):
  """
tracepeph(int level, const nav_t *nav)"""

  if(type(nav) == nav_t):
    nav = ctypes.byref(nav)

  result = rtklib.tracepeph(level,nav)


  return result

rtklib.tracepclk.argtypes = [ctypes.c_int,ctypes.POINTER(nav_t)]
rtklib.tracepclk.restype = None
def tracepclk(level,nav):
  """
tracepclk(int level, const nav_t *nav)"""

  if(type(nav) == nav_t):
    nav = ctypes.byref(nav)

  result = rtklib.tracepclk(level,nav)


  return result

rtklib.traceb.argtypes = [ctypes.c_int,ctypes.POINTER(ctypes.c_ubyte),ctypes.c_int]
rtklib.traceb.restype = None
def traceb(level,p,n):
  """
traceb   (int level, const unsigned char *p, int n)"""

  result = rtklib.traceb(level,p,n)


  return result

rtklib.execcmd.argtypes = [ctypes.POINTER(ctypes.c_char)]
rtklib.execcmd.restype = ctypes.c_int
def execcmd(cmd):
  """
execcmd(const char *cmd)"""

  result = rtklib.execcmd(cmd)


  return result

rtklib.createdir.argtypes = [ctypes.POINTER(ctypes.c_char)]
rtklib.createdir.restype = None
def createdir(path):
  """
createdir(const char *path)"""

  result = rtklib.createdir(path)


  return result

rtklib.satwavelen.argtypes = [ctypes.c_int,ctypes.c_int,ctypes.POINTER(nav_t)]
rtklib.satwavelen.restype = ctypes.c_double
def satwavelen(sat,frq,nav):
  """
satwavelen(int sat, int frq, const nav_t *nav)"""

  if(type(nav) == nav_t):
    nav = ctypes.byref(nav)

  result = rtklib.satwavelen(sat,frq,nav)


  return result

rtklib.satazel.argtypes = [ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
rtklib.satazel.restype = ctypes.c_double
def satazel(pos,e,azel):
  """
satazel(const double *pos, const double *e, double *azel)"""

  result = rtklib.satazel(pos,e,azel)


  return result

rtklib.geodist.argtypes = [ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
rtklib.geodist.restype = ctypes.c_double
def geodist(rs,rr,e):
  """
geodist(const double *rs, const double *rr, double *e)"""

  result = rtklib.geodist(rs,rr,e)


  return result

rtklib.dops.argtypes = [ctypes.c_int,ctypes.POINTER(ctypes.c_double),ctypes.c_double,ctypes.POINTER(ctypes.c_double)]
rtklib.dops.restype = None
def dops(ns,azel,elmin,dop):
  """
dops(int ns, const double *azel, double elmin, double *dop)"""

  result = rtklib.dops(ns,azel,elmin,dop)


  return result

rtklib.csmooth.argtypes = [ctypes.POINTER(obs_t),ctypes.c_int]
rtklib.csmooth.restype = None
def csmooth(obs,ns):
  """
csmooth(obs_t *obs, int ns)"""

  if(type(obs) == obs_t):
    obs = ctypes.byref(obs)

  result = rtklib.csmooth(obs,ns)


  return result

rtklib.ionmodel.argtypes = [gtime_t,ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
rtklib.ionmodel.restype = ctypes.c_double
def ionmodel(t,ion,pos,azel):
  """
ionmodel(gtime_t t, const double *ion, const double *pos,
                       const double *azel)"""

  result = rtklib.ionmodel(t,ion,pos,azel)


  return result

rtklib.ionmapf.argtypes = [ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
rtklib.ionmapf.restype = ctypes.c_double
def ionmapf(pos,azel):
  """
ionmapf(const double *pos, const double *azel)"""

  result = rtklib.ionmapf(pos,azel)


  return result

rtklib.ionppp.argtypes = [ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.c_double,ctypes.c_double,ctypes.POINTER(ctypes.c_double)]
rtklib.ionppp.restype = ctypes.c_double
def ionppp(pos,azel,re,hion,pppos):
  """
ionppp(const double *pos, const double *azel, double re,
                     double hion, double *pppos)"""

  result = rtklib.ionppp(pos,azel,re,hion,pppos)


  return result

rtklib.tropmodel.argtypes = [gtime_t,ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.c_double]
rtklib.tropmodel.restype = ctypes.c_double
def tropmodel(time,pos,azel,humi):
  """
tropmodel(gtime_t time, const double *pos, const double *azel,
                        double humi)"""

  result = rtklib.tropmodel(time,pos,azel,humi)


  return result

rtklib.tropmapf.argtypes = [gtime_t,ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
rtklib.tropmapf.restype = ctypes.c_double
def tropmapf(time,pos,azel,mapfw):
  """
tropmapf(gtime_t time, const double *pos, const double *azel,
                       double *mapfw)"""

  result = rtklib.tropmapf(time,pos,azel,mapfw)


  return result

rtklib.iontec.argtypes = [gtime_t,ctypes.POINTER(nav_t),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.c_int,ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
rtklib.iontec.restype = ctypes.c_int
def iontec(time,nav,pos,azel,opt,delay,var):
  """
iontec(gtime_t time, const nav_t *nav, const double *pos,
                  const double *azel, int opt, double *delay, double *var)"""

  if(type(nav) == nav_t):
    nav = ctypes.byref(nav)

  result = rtklib.iontec(time,nav,pos,azel,opt,delay,var)


  return result

rtklib.readtec.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.POINTER(nav_t),ctypes.c_int]
rtklib.readtec.restype = None
def readtec(file,nav,opt):
  """
readtec(const char *file, nav_t *nav, int opt)"""

  if(type(nav) == nav_t):
    nav = ctypes.byref(nav)

  result = rtklib.readtec(file,nav,opt)


  return result

rtklib.ionocorr.argtypes = [gtime_t,ctypes.POINTER(nav_t),ctypes.c_int,ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.c_int,ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
rtklib.ionocorr.restype = ctypes.c_int
def ionocorr(time,nav,sat,pos,azel,ionoopt,ion,var):
  """
ionocorr(gtime_t time, const nav_t *nav, int sat, const double *pos,
                    const double *azel, int ionoopt, double *ion, double *var)"""

  if(type(nav) == nav_t):
    nav = ctypes.byref(nav)

  result = rtklib.ionocorr(time,nav,sat,pos,azel,ionoopt,ion,var)


  return result

rtklib.tropcorr.argtypes = [gtime_t,ctypes.POINTER(nav_t),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.c_int,ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
rtklib.tropcorr.restype = ctypes.c_int
def tropcorr(time,nav,pos,azel,tropopt,trp,var):
  """
tropcorr(gtime_t time, const nav_t *nav, const double *pos,
                    const double *azel, int tropopt, double *trp, double *var)"""

  if(type(nav) == nav_t):
    nav = ctypes.byref(nav)

  result = rtklib.tropcorr(time,nav,pos,azel,tropopt,trp,var)


  return result

rtklib.readpcv.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.POINTER(pcvs_t)]
rtklib.readpcv.restype = ctypes.c_int
def readpcv(file,pcvs):
  """
readpcv(const char *file, pcvs_t *pcvs)"""

  if(type(pcvs) == pcvs_t):
    pcvs = ctypes.byref(pcvs)

  result = rtklib.readpcv(file,pcvs)


  return result

rtklib.searchpcv.argtypes = [ctypes.c_int,ctypes.POINTER(ctypes.c_char),gtime_t,ctypes.POINTER(pcvs_t)]
rtklib.searchpcv.restype = ctypes.POINTER(pcv_t)
def searchpcv(sat,type,time,pcvs):
  """
searchpcv(int sat, const char *type, gtime_t time,
                        const pcvs_t *pcvs)"""

  if(type(pcvs) == pcvs_t):
    pcvs = ctypes.byref(pcvs)

  result = rtklib.searchpcv(sat,type,time,pcvs)


  return result

rtklib.antmodel.argtypes = [ctypes.POINTER(pcv_t),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.c_int,ctypes.POINTER(ctypes.c_double)]
rtklib.antmodel.restype = None
def antmodel(pcv,Del,azel,opt,dant):
  """
antmodel(const pcv_t *pcv, const double *Del, const double *azel,
                     int opt, double *dant)"""

  if(type(pcv) == pcv_t):
    pcv = ctypes.byref(pcv)

  result = rtklib.antmodel(pcv,Del,azel,opt,dant)


  return result

rtklib.antmodel_s.argtypes = [ctypes.POINTER(pcv_t),ctypes.c_double,ctypes.POINTER(ctypes.c_double)]
rtklib.antmodel_s.restype = None
def antmodel_s(pcv,nadir,dant):
  """
antmodel_s(const pcv_t *pcv, double nadir, double *dant)"""

  if(type(pcv) == pcv_t):
    pcv = ctypes.byref(pcv)

  result = rtklib.antmodel_s(pcv,nadir,dant)


  return result

rtklib.sunmoonpos.argtypes = [gtime_t,ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
rtklib.sunmoonpos.restype = None
def sunmoonpos(tutc,erpv,rsun,rmoon,gmst):
  """
sunmoonpos(gtime_t tutc, const double *erpv, double *rsun,
                       double *rmoon, double *gmst)"""

  result = rtklib.sunmoonpos(tutc,erpv,rsun,rmoon,gmst)


  return result

rtklib.tidedisp.argtypes = [gtime_t,ctypes.POINTER(ctypes.c_double),ctypes.c_int,ctypes.POINTER(erp_t),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
rtklib.tidedisp.restype = None
def tidedisp(tutc,rr,opt,erp,odisp,dr):
  """
tidedisp(gtime_t tutc, const double *rr, int opt, const erp_t *erp,
                     const double *odisp, double *dr)"""

  if(type(erp) == erp_t):
    erp = ctypes.byref(erp)

  result = rtklib.tidedisp(tutc,rr,opt,erp,odisp,dr)


  return result

rtklib.opengeoid.argtypes = [ctypes.c_int,ctypes.POINTER(ctypes.c_char)]
rtklib.opengeoid.restype = ctypes.c_int
def opengeoid(model,file):
  """
opengeoid(int model, const char *file)"""

  result = rtklib.opengeoid(model,file)


  return result

rtklib.closegeoid.argtypes = []
rtklib.closegeoid.restype = None
def closegeoid():
  """
closegeoid(void)"""

  result = rtklib.closegeoid()


  return result

rtklib.geoidh.argtypes = [ctypes.POINTER(ctypes.c_double)]
rtklib.geoidh.restype = ctypes.c_double
def geoidh(pos):
  """
geoidh(const double *pos)"""

  result = rtklib.geoidh(pos)


  return result

rtklib.loaddatump.argtypes = [ctypes.POINTER(ctypes.c_char)]
rtklib.loaddatump.restype = ctypes.c_int
def loaddatump(file):
  """
loaddatump(const char *file)"""

  result = rtklib.loaddatump(file)


  return result

rtklib.tokyo2jgd.argtypes = [ctypes.POINTER(ctypes.c_double)]
rtklib.tokyo2jgd.restype = ctypes.c_int
def tokyo2jgd(pos):
  """
tokyo2jgd(double *pos)"""

  result = rtklib.tokyo2jgd(pos)


  return result

rtklib.jgd2tokyo.argtypes = [ctypes.POINTER(ctypes.c_double)]
rtklib.jgd2tokyo.restype = ctypes.c_int
def jgd2tokyo(pos):
  """
jgd2tokyo(double *pos)"""

  result = rtklib.jgd2tokyo(pos)


  return result

rtklib.readrnx.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.c_int,ctypes.POINTER(ctypes.c_char),ctypes.POINTER(obs_t),ctypes.POINTER(nav_t),ctypes.POINTER(sta_t)]
rtklib.readrnx.restype = ctypes.c_int
def readrnx(file,rcv,opt,obs,nav,sta):
  """
readrnx (const char *file, int rcv, const char *opt, obs_t *obs,
                    nav_t *nav, sta_t *sta)"""

  if(type(obs) == obs_t):
    obs = ctypes.byref(obs)

  if(type(nav) == nav_t):
    nav = ctypes.byref(nav)

  if(type(sta) == sta_t):
    sta = ctypes.byref(sta)

  result = rtklib.readrnx(file,rcv,opt,obs,nav,sta)


  return result

rtklib.readrnxt.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.c_int,gtime_t,gtime_t,ctypes.c_double,ctypes.POINTER(ctypes.c_char),ctypes.POINTER(obs_t),ctypes.POINTER(nav_t),ctypes.POINTER(sta_t)]
rtklib.readrnxt.restype = ctypes.c_int
def readrnxt(file,rcv,ts,te,tint,opt,obs,nav,sta):
  """/*!
* @brief read rinex obs and nav files
* args   : char *file    I      file (wild-card * expanded) ("": stdin)
*          int   rcv     I      receiver number for obs data
*         (gtime_t ts)   I      observation time start (ts.time==0: no limit)
*         (gtime_t te)   I      observation time end   (te.time==0: no limit)
*         (double tint)  I      observation time interval (s) (0:all)
*          char  *opt    I      rinex options (see below,"": no option)
*          obs_t *obs    IO     observation data   (NULL: no input)
*          nav_t *nav    IO     navigation data    (NULL: no input)
*          sta_t *sta    IO     station parameters (NULL: no input)
* return : status (1:ok,0:no data,-1:error)
* notes  : read data are appended to obs and nav struct
*          before calling the function, obs and nav should be initialized.
*          observation data and navigation data are not sorted.
*          navigation data may be duplicated.
*          call sortobs() or uniqnav() to sort data or delete duplicated eph.
*
*          rinex options (separated by spaces) :
*
*            -GLss[=shift]: select GPS signal ss (ss: RINEX 3 code, "1C","2W"...)
*            -RLss[=shift]: select GLO signal ss
*            -ELss[=shift]: select GAL signal ss
*            -JLss[=shift]: select QZS signal ss
*            -CLss[=shift]: select BDS signal ss
*            -SLss[=shift]: select SBS signal ss
*
*            shift: carrier phase shift to be added (cycle)
*
*-----------------------------------------------------------------------------*/
readrnxt(const char *file, int rcv, gtime_t ts, gtime_t te,
                    double tint, const char *opt, obs_t *obs, nav_t *nav,
                    sta_t *sta)"""

  if(type(obs) == obs_t):
    obs = ctypes.byref(obs)

  if(type(nav) == nav_t):
    nav = ctypes.byref(nav)

  if(type(sta) == sta_t):
    sta = ctypes.byref(sta)

  result = rtklib.readrnxt(file,rcv,ts,te,tint,opt,obs,nav,sta)


  return result

rtklib.readrnxc.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.POINTER(nav_t)]
rtklib.readrnxc.restype = ctypes.c_int
def readrnxc(file,nav):
  """
readrnxc(const char *file, nav_t *nav)"""

  if(type(nav) == nav_t):
    nav = ctypes.byref(nav)

  result = rtklib.readrnxc(file,nav)


  return result

rtklib.outrnxobsh.argtypes = [ctypes.POINTER(None),ctypes.POINTER(rnxopt_t),ctypes.POINTER(nav_t)]
rtklib.outrnxobsh.restype = ctypes.c_int
def outrnxobsh(fp,opt,nav):
  """
outrnxobsh(FILE *fp, const rnxopt_t *opt, const nav_t *nav)"""

  if(type(opt) == rnxopt_t):
    opt = ctypes.byref(opt)

  if(type(nav) == nav_t):
    nav = ctypes.byref(nav)

  result = rtklib.outrnxobsh(fp,opt,nav)


  return result

rtklib.outrnxobsb.argtypes = [ctypes.POINTER(None),ctypes.POINTER(rnxopt_t),ctypes.POINTER(obsd_t),ctypes.c_int,ctypes.c_int]
rtklib.outrnxobsb.restype = ctypes.c_int
def outrnxobsb(fp,opt,obs,n,epflag):
  """/*!
* output rinex obs body -------------------------------------------------------
* output rinex obs body
* args   : FILE   *fp       I   output file pointer
*          rnxopt_t *opt    I   rinex options
*          obsd_t *obs      I   observation data
*          int    n         I   number of observation data
*          int    flag      I   epoch flag (0:ok,1:power failure,>1:event flag)
* return : status (1:ok, 0:output error)
*-----------------------------------------------------------------------------*/
outrnxobsb(FILE *fp, const rnxopt_t *opt, const obsd_t *obs, int n,
                      int epflag)"""

  if(type(opt) == rnxopt_t):
    opt = ctypes.byref(opt)

  if(type(obs) == obsd_t):
    obs = ctypes.byref(obs)

  result = rtklib.outrnxobsb(fp,opt,obs,n,epflag)


  return result

rtklib.outrnxnavh.argtypes = [ctypes.POINTER(None),ctypes.POINTER(rnxopt_t),ctypes.POINTER(nav_t)]
rtklib.outrnxnavh.restype = ctypes.c_int
def outrnxnavh(fp,opt,nav):
  """
outrnxnavh (FILE *fp, const rnxopt_t *opt, const nav_t *nav)"""

  if(type(opt) == rnxopt_t):
    opt = ctypes.byref(opt)

  if(type(nav) == nav_t):
    nav = ctypes.byref(nav)

  result = rtklib.outrnxnavh(fp,opt,nav)


  return result

rtklib.outrnxgnavh.argtypes = [ctypes.POINTER(None),ctypes.POINTER(rnxopt_t),ctypes.POINTER(nav_t)]
rtklib.outrnxgnavh.restype = ctypes.c_int
def outrnxgnavh(fp,opt,nav):
  """
outrnxgnavh(FILE *fp, const rnxopt_t *opt, const nav_t *nav)"""

  if(type(opt) == rnxopt_t):
    opt = ctypes.byref(opt)

  if(type(nav) == nav_t):
    nav = ctypes.byref(nav)

  result = rtklib.outrnxgnavh(fp,opt,nav)


  return result

rtklib.outrnxhnavh.argtypes = [ctypes.POINTER(None),ctypes.POINTER(rnxopt_t),ctypes.POINTER(nav_t)]
rtklib.outrnxhnavh.restype = ctypes.c_int
def outrnxhnavh(fp,opt,nav):
  """
outrnxhnavh(FILE *fp, const rnxopt_t *opt, const nav_t *nav)"""

  if(type(opt) == rnxopt_t):
    opt = ctypes.byref(opt)

  if(type(nav) == nav_t):
    nav = ctypes.byref(nav)

  result = rtklib.outrnxhnavh(fp,opt,nav)


  return result

rtklib.outrnxlnavh.argtypes = [ctypes.POINTER(None),ctypes.POINTER(rnxopt_t),ctypes.POINTER(nav_t)]
rtklib.outrnxlnavh.restype = ctypes.c_int
def outrnxlnavh(fp,opt,nav):
  """
outrnxlnavh(FILE *fp, const rnxopt_t *opt, const nav_t *nav)"""

  if(type(opt) == rnxopt_t):
    opt = ctypes.byref(opt)

  if(type(nav) == nav_t):
    nav = ctypes.byref(nav)

  result = rtklib.outrnxlnavh(fp,opt,nav)


  return result

rtklib.outrnxqnavh.argtypes = [ctypes.POINTER(None),ctypes.POINTER(rnxopt_t),ctypes.POINTER(nav_t)]
rtklib.outrnxqnavh.restype = ctypes.c_int
def outrnxqnavh(fp,opt,nav):
  """
outrnxqnavh(FILE *fp, const rnxopt_t *opt, const nav_t *nav)"""

  if(type(opt) == rnxopt_t):
    opt = ctypes.byref(opt)

  if(type(nav) == nav_t):
    nav = ctypes.byref(nav)

  result = rtklib.outrnxqnavh(fp,opt,nav)


  return result

rtklib.outrnxcnavh.argtypes = [ctypes.POINTER(None),ctypes.POINTER(rnxopt_t),ctypes.POINTER(nav_t)]
rtklib.outrnxcnavh.restype = ctypes.c_int
def outrnxcnavh(fp,opt,nav):
  """
outrnxcnavh(FILE *fp, const rnxopt_t *opt, const nav_t *nav)"""

  if(type(opt) == rnxopt_t):
    opt = ctypes.byref(opt)

  if(type(nav) == nav_t):
    nav = ctypes.byref(nav)

  result = rtklib.outrnxcnavh(fp,opt,nav)


  return result

rtklib.outrnxnavb.argtypes = [ctypes.POINTER(None),ctypes.POINTER(rnxopt_t),ctypes.POINTER(eph_t)]
rtklib.outrnxnavb.restype = ctypes.c_int
def outrnxnavb(fp,opt,eph):
  """
outrnxnavb (FILE *fp, const rnxopt_t *opt, const eph_t *eph)"""

  if(type(opt) == rnxopt_t):
    opt = ctypes.byref(opt)

  if(type(eph) == eph_t):
    eph = ctypes.byref(eph)

  result = rtklib.outrnxnavb(fp,opt,eph)


  return result

rtklib.outrnxgnavb.argtypes = [ctypes.POINTER(None),ctypes.POINTER(rnxopt_t),ctypes.POINTER(geph_t)]
rtklib.outrnxgnavb.restype = ctypes.c_int
def outrnxgnavb(fp,opt,geph):
  """
outrnxgnavb(FILE *fp, const rnxopt_t *opt, const geph_t *geph)"""

  if(type(opt) == rnxopt_t):
    opt = ctypes.byref(opt)

  if(type(geph) == geph_t):
    geph = ctypes.byref(geph)

  result = rtklib.outrnxgnavb(fp,opt,geph)


  return result

rtklib.outrnxhnavb.argtypes = [ctypes.POINTER(None),ctypes.POINTER(rnxopt_t),ctypes.POINTER(seph_t)]
rtklib.outrnxhnavb.restype = ctypes.c_int
def outrnxhnavb(fp,opt,seph):
  """
outrnxhnavb(FILE *fp, const rnxopt_t *opt, const seph_t *seph)"""

  if(type(opt) == rnxopt_t):
    opt = ctypes.byref(opt)

  if(type(seph) == seph_t):
    seph = ctypes.byref(seph)

  result = rtklib.outrnxhnavb(fp,opt,seph)


  return result

rtklib.uncompress.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.POINTER(ctypes.c_char)]
rtklib.uncompress.restype = ctypes.c_int
def uncompress(file,uncfile):
  """
uncompress(const char *file, char *uncfile)"""

  result = rtklib.uncompress(file,uncfile)


  return result

rtklib.convrnx.argtypes = [ctypes.c_int,ctypes.POINTER(rnxopt_t),ctypes.POINTER(ctypes.c_char),ctypes.POINTER(ctypes.c_void_p)]
rtklib.convrnx.restype = ctypes.c_int
def convrnx(format,opt,file,ofile):
  """
convrnx(int format, rnxopt_t *opt, const char *file, char **ofile)"""

  if(type(opt) == rnxopt_t):
    opt = ctypes.byref(opt)

  result = rtklib.convrnx(format,opt,file,ofile)


  return result

rtklib.init_rnxctr.argtypes = [ctypes.POINTER(rnxctr_t)]
rtklib.init_rnxctr.restype = ctypes.c_int
def init_rnxctr(rnx):
  """
init_rnxctr (rnxctr_t *rnx)"""

  if(type(rnx) == rnxctr_t):
    rnx = ctypes.byref(rnx)

  result = rtklib.init_rnxctr(rnx)


  return result

rtklib.free_rnxctr.argtypes = [ctypes.POINTER(rnxctr_t)]
rtklib.free_rnxctr.restype = None
def free_rnxctr(rnx):
  """
free_rnxctr (rnxctr_t *rnx)"""

  if(type(rnx) == rnxctr_t):
    rnx = ctypes.byref(rnx)

  result = rtklib.free_rnxctr(rnx)


  return result

rtklib.eph2clk.argtypes = [gtime_t,ctypes.POINTER(eph_t)]
rtklib.eph2clk.restype = ctypes.c_double
def eph2clk(time,eph):
  """
eph2clk (gtime_t time, const eph_t  *eph)"""

  if(type(eph) == eph_t):
    eph = ctypes.byref(eph)

  result = rtklib.eph2clk(time,eph)


  return result

rtklib.geph2clk.argtypes = [gtime_t,ctypes.POINTER(geph_t)]
rtklib.geph2clk.restype = ctypes.c_double
def geph2clk(time,geph):
  """
geph2clk(gtime_t time, const geph_t *geph)"""

  if(type(geph) == geph_t):
    geph = ctypes.byref(geph)

  result = rtklib.geph2clk(time,geph)


  return result

rtklib.seph2clk.argtypes = [gtime_t,ctypes.POINTER(seph_t)]
rtklib.seph2clk.restype = ctypes.c_double
def seph2clk(time,seph):
  """
seph2clk(gtime_t time, const seph_t *seph)"""

  if(type(seph) == seph_t):
    seph = ctypes.byref(seph)

  result = rtklib.seph2clk(time,seph)


  return result

rtklib.eph2pos.argtypes = [gtime_t,ctypes.POINTER(eph_t),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
rtklib.eph2pos.restype = None
def eph2pos(time,eph,rs,dts,var):
  """
eph2pos (gtime_t time, const eph_t  *eph,  double *rs, double *dts,
                     double *var)"""

  if(type(eph) == eph_t):
    eph = ctypes.byref(eph)

  result = rtklib.eph2pos(time,eph,rs,dts,var)


  return result

rtklib.geph2pos.argtypes = [gtime_t,ctypes.POINTER(geph_t),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
rtklib.geph2pos.restype = None
def geph2pos(time,geph,rs,dts,var):
  """
geph2pos(gtime_t time, const geph_t *geph, double *rs, double *dts,
                     double *var)"""

  if(type(geph) == geph_t):
    geph = ctypes.byref(geph)

  result = rtklib.geph2pos(time,geph,rs,dts,var)


  return result

rtklib.seph2pos.argtypes = [gtime_t,ctypes.POINTER(seph_t),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
rtklib.seph2pos.restype = None
def seph2pos(time,seph,rs,dts,var):
  """
seph2pos(gtime_t time, const seph_t *seph, double *rs, double *dts,
                     double *var)"""

  if(type(seph) == seph_t):
    seph = ctypes.byref(seph)

  result = rtklib.seph2pos(time,seph,rs,dts,var)


  return result

rtklib.peph2pos.argtypes = [gtime_t,ctypes.c_int,ctypes.POINTER(nav_t),ctypes.c_int,ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
rtklib.peph2pos.restype = ctypes.c_int
def peph2pos(time,sat,nav,opt,rs,dts,var):
  """
peph2pos(gtime_t time, int sat, const nav_t *nav, int opt,
                     double *rs, double *dts, double *var)"""

  if(type(nav) == nav_t):
    nav = ctypes.byref(nav)

  result = rtklib.peph2pos(time,sat,nav,opt,rs,dts,var)


  return result

rtklib.satantoff.argtypes = [gtime_t,ctypes.POINTER(ctypes.c_double),ctypes.c_int,ctypes.POINTER(nav_t),ctypes.POINTER(ctypes.c_double)]
rtklib.satantoff.restype = None
def satantoff(time,rs,sat,nav,dant):
  """
satantoff(gtime_t time, const double *rs, int sat, const nav_t *nav,
                      double *dant)"""

  if(type(nav) == nav_t):
    nav = ctypes.byref(nav)

  result = rtklib.satantoff(time,rs,sat,nav,dant)


  return result

rtklib.satpos.argtypes = [gtime_t,gtime_t,ctypes.c_int,ctypes.c_int,ctypes.POINTER(nav_t),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_int)]
rtklib.satpos.restype = ctypes.c_int
def satpos(time,teph,sat,ephopt,nav,rs,dts,var,svh):
  """
satpos(gtime_t time, gtime_t teph, int sat, int ephopt,
                   const nav_t *nav, double *rs, double *dts, double *var,
                   int *svh)"""

  if(type(nav) == nav_t):
    nav = ctypes.byref(nav)

  result = rtklib.satpos(time,teph,sat,ephopt,nav,rs,dts,var,svh)


  return result

rtklib.satposs.argtypes = [gtime_t,ctypes.POINTER(obsd_t),ctypes.c_int,ctypes.POINTER(nav_t),ctypes.c_int,ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_int)]
rtklib.satposs.restype = None
def satposs(time,obs,n,nav,sateph,rs,dts,var,svh):
  """
satposs(gtime_t time, const obsd_t *obs, int n, const nav_t *nav,
                    int sateph, double *rs, double *dts, double *var, int *svh)"""

  if(type(obs) == obsd_t):
    obs = ctypes.byref(obs)

  if(type(nav) == nav_t):
    nav = ctypes.byref(nav)

  result = rtklib.satposs(time,obs,n,nav,sateph,rs,dts,var,svh)


  return result

rtklib.readsp3.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.POINTER(nav_t),ctypes.c_int]
rtklib.readsp3.restype = None
def readsp3(file,nav,opt):
  """
readsp3(const char *file, nav_t *nav, int opt)"""

  if(type(nav) == nav_t):
    nav = ctypes.byref(nav)

  result = rtklib.readsp3(file,nav,opt)


  return result

rtklib.readsap.argtypes = [ctypes.POINTER(ctypes.c_char),gtime_t,ctypes.POINTER(nav_t)]
rtklib.readsap.restype = ctypes.c_int
def readsap(file,time,nav):
  """
readsap(const char *file, gtime_t time, nav_t *nav)"""

  if(type(nav) == nav_t):
    nav = ctypes.byref(nav)

  result = rtklib.readsap(file,time,nav)


  return result

rtklib.readdcb.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.POINTER(nav_t)]
rtklib.readdcb.restype = ctypes.c_int
def readdcb(file,nav):
  """
readdcb(const char *file, nav_t *nav)"""

  if(type(nav) == nav_t):
    nav = ctypes.byref(nav)

  result = rtklib.readdcb(file,nav)


  return result

rtklib.alm2pos.argtypes = [gtime_t,ctypes.POINTER(alm_t),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
rtklib.alm2pos.restype = None
def alm2pos(time,alm,rs,dts):
  """
alm2pos(gtime_t time, const alm_t *alm, double *rs, double *dts)"""

  if(type(alm) == alm_t):
    alm = ctypes.byref(alm)

  result = rtklib.alm2pos(time,alm,rs,dts)


  return result

rtklib.tle_read.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.POINTER(tle_t)]
rtklib.tle_read.restype = ctypes.c_int
def tle_read(file,tle):
  """
tle_read(const char *file, tle_t *tle)"""

  if(type(tle) == tle_t):
    tle = ctypes.byref(tle)

  result = rtklib.tle_read(file,tle)


  return result

rtklib.tle_name_read.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.POINTER(tle_t)]
rtklib.tle_name_read.restype = ctypes.c_int
def tle_name_read(file,tle):
  """
tle_name_read(const char *file, tle_t *tle)"""

  if(type(tle) == tle_t):
    tle = ctypes.byref(tle)

  result = rtklib.tle_name_read(file,tle)


  return result

rtklib.tle_pos.argtypes = [gtime_t,ctypes.POINTER(ctypes.c_char),ctypes.POINTER(ctypes.c_char),ctypes.POINTER(ctypes.c_char),ctypes.POINTER(tle_t),ctypes.POINTER(erp_t),ctypes.POINTER(ctypes.c_double)]
rtklib.tle_pos.restype = ctypes.c_int
def tle_pos(time,name,satno,desig,tle,erp,rs):
  """
tle_pos(gtime_t time, const char *name, const char *satno,
                   const char *desig, const tle_t *tle, const erp_t *erp,
                   double *rs)"""

  if(type(tle) == tle_t):
    tle = ctypes.byref(tle)

  if(type(erp) == erp_t):
    erp = ctypes.byref(erp)

  result = rtklib.tle_pos(time,name,satno,desig,tle,erp,rs)


  return result

rtklib.getbitu.argtypes = [ctypes.POINTER(ctypes.c_ubyte),ctypes.c_int,ctypes.c_int]
rtklib.getbitu.restype = ctypes.c_uint
def getbitu(buff,pos,len):
  """
getbitu(const unsigned char *buff, int pos, int len)"""

  result = rtklib.getbitu(buff,pos,len)


  return result

rtklib.getbits.argtypes = [ctypes.POINTER(ctypes.c_ubyte),ctypes.c_int,ctypes.c_int]
rtklib.getbits.restype = ctypes.c_int
def getbits(buff,pos,len):
  """
getbits(const unsigned char *buff, int pos, int len)"""

  result = rtklib.getbits(buff,pos,len)


  return result

rtklib.setbitu.argtypes = [ctypes.POINTER(ctypes.c_ubyte),ctypes.c_int,ctypes.c_int,ctypes.c_uint]
rtklib.setbitu.restype = None
def setbitu(buff,pos,len,data):
  """
setbitu(unsigned char *buff, int pos, int len, unsigned int data)"""

  result = rtklib.setbitu(buff,pos,len,data)


  return result

rtklib.setbits.argtypes = [ctypes.POINTER(ctypes.c_ubyte),ctypes.c_int,ctypes.c_int,ctypes.c_int]
rtklib.setbits.restype = None
def setbits(buff,pos,len,data):
  """
setbits(unsigned char *buff, int pos, int len, int data)"""

  result = rtklib.setbits(buff,pos,len,data)


  return result

rtklib.crc32.argtypes = [ctypes.POINTER(ctypes.c_ubyte),ctypes.c_int]
rtklib.crc32.restype = ctypes.c_uint
def crc32(buff,len):
  """
crc32  (const unsigned char *buff, int len)"""

  result = rtklib.crc32(buff,len)


  return result

rtklib.crc24q.argtypes = [ctypes.POINTER(ctypes.c_ubyte),ctypes.c_int]
rtklib.crc24q.restype = ctypes.c_uint
def crc24q(buff,len):
  """
crc24q (const unsigned char *buff, int len)"""

  result = rtklib.crc24q(buff,len)


  return result

rtklib.crc16.argtypes = [ctypes.POINTER(ctypes.c_ubyte),ctypes.c_int]
rtklib.crc16.restype = ctypes.c_ushort
def crc16(buff,len):
  """
crc16(const unsigned char *buff, int len)"""

  result = rtklib.crc16(buff,len)


  return result

rtklib.decode_word.argtypes = [ctypes.c_uint,ctypes.POINTER(ctypes.c_ubyte)]
rtklib.decode_word.restype = ctypes.c_int
def decode_word(word,data):
  """
decode_word (unsigned int word, unsigned char *data)"""

  result = rtklib.decode_word(word,data)


  return result

rtklib.decode_frame.argtypes = [ctypes.POINTER(ctypes.c_ubyte),ctypes.POINTER(eph_t),ctypes.POINTER(alm_t),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_int)]
rtklib.decode_frame.restype = ctypes.c_int
def decode_frame(buff,eph,alm,ion,utc,leaps):
  """
decode_frame(const unsigned char *buff, eph_t *eph, alm_t *alm,
                        double *ion, double *utc, int *leaps)"""

  if(type(eph) == eph_t):
    eph = ctypes.byref(eph)

  if(type(alm) == alm_t):
    alm = ctypes.byref(alm)

  result = rtklib.decode_frame(buff,eph,alm,ion,utc,leaps)


  return result

rtklib.test_glostr.argtypes = [ctypes.POINTER(ctypes.c_ubyte)]
rtklib.test_glostr.restype = ctypes.c_int
def test_glostr(buff):
  """
test_glostr(const unsigned char *buff)"""

  result = rtklib.test_glostr(buff)


  return result

rtklib.decode_glostr.argtypes = [ctypes.POINTER(ctypes.c_ubyte),ctypes.POINTER(geph_t)]
rtklib.decode_glostr.restype = ctypes.c_int
def decode_glostr(buff,geph):
  """
decode_glostr(const unsigned char *buff, geph_t *geph)"""

  if(type(geph) == geph_t):
    geph = ctypes.byref(geph)

  result = rtklib.decode_glostr(buff,geph)


  return result

rtklib.decode_bds_d1.argtypes = [ctypes.POINTER(ctypes.c_ubyte),ctypes.POINTER(eph_t)]
rtklib.decode_bds_d1.restype = ctypes.c_int
def decode_bds_d1(buff,eph):
  """
decode_bds_d1(const unsigned char *buff, eph_t *eph)"""

  if(type(eph) == eph_t):
    eph = ctypes.byref(eph)

  result = rtklib.decode_bds_d1(buff,eph)


  return result

rtklib.decode_bds_d2.argtypes = [ctypes.POINTER(ctypes.c_ubyte),ctypes.POINTER(eph_t)]
rtklib.decode_bds_d2.restype = ctypes.c_int
def decode_bds_d2(buff,eph):
  """
decode_bds_d2(const unsigned char *buff, eph_t *eph)"""

  if(type(eph) == eph_t):
    eph = ctypes.byref(eph)

  result = rtklib.decode_bds_d2(buff,eph)


  return result

rtklib.init_raw.argtypes = [ctypes.POINTER(raw_t)]
rtklib.init_raw.restype = ctypes.c_int
def init_raw(raw):
  """
init_raw   (raw_t *raw)"""

  if(type(raw) == raw_t):
    raw = ctypes.byref(raw)

  result = rtklib.init_raw(raw)


  return result

rtklib.free_raw.argtypes = [ctypes.POINTER(raw_t)]
rtklib.free_raw.restype = None
def free_raw(raw):
  """
free_raw  (raw_t *raw)"""

  if(type(raw) == raw_t):
    raw = ctypes.byref(raw)

  result = rtklib.free_raw(raw)


  return result

rtklib.input_raw.argtypes = [ctypes.POINTER(raw_t),ctypes.c_int,ctypes.c_ubyte]
rtklib.input_raw.restype = ctypes.c_int
def input_raw(raw,format,data):
  """
input_raw  (raw_t *raw, int format, unsigned char data)"""

  if(type(raw) == raw_t):
    raw = ctypes.byref(raw)

  result = rtklib.input_raw(raw,format,data)


  return result

rtklib.input_rawf.argtypes = [ctypes.POINTER(raw_t),ctypes.c_int,ctypes.POINTER(None)]
rtklib.input_rawf.restype = ctypes.c_int
def input_rawf(raw,format,fp):
  """
input_rawf (raw_t *raw, int format, FILE *fp)"""

  if(type(raw) == raw_t):
    raw = ctypes.byref(raw)

  result = rtklib.input_rawf(raw,format,fp)


  return result

rtklib.input_oem4.argtypes = [ctypes.POINTER(raw_t),ctypes.c_ubyte]
rtklib.input_oem4.restype = ctypes.c_int
def input_oem4(raw,data):
  """
input_oem4  (raw_t *raw, unsigned char data)"""

  if(type(raw) == raw_t):
    raw = ctypes.byref(raw)

  result = rtklib.input_oem4(raw,data)


  return result

rtklib.input_oem3.argtypes = [ctypes.POINTER(raw_t),ctypes.c_ubyte]
rtklib.input_oem3.restype = ctypes.c_int
def input_oem3(raw,data):
  """
input_oem3  (raw_t *raw, unsigned char data)"""

  if(type(raw) == raw_t):
    raw = ctypes.byref(raw)

  result = rtklib.input_oem3(raw,data)


  return result

rtklib.input_ubx.argtypes = [ctypes.POINTER(raw_t),ctypes.c_ubyte]
rtklib.input_ubx.restype = ctypes.c_int
def input_ubx(raw,data):
  """
input_ubx   (raw_t *raw, unsigned char data)"""

  if(type(raw) == raw_t):
    raw = ctypes.byref(raw)

  result = rtklib.input_ubx(raw,data)


  return result

rtklib.input_ss2.argtypes = [ctypes.POINTER(raw_t),ctypes.c_ubyte]
rtklib.input_ss2.restype = ctypes.c_int
def input_ss2(raw,data):
  """
input_ss2   (raw_t *raw, unsigned char data)"""

  if(type(raw) == raw_t):
    raw = ctypes.byref(raw)

  result = rtklib.input_ss2(raw,data)


  return result

rtklib.input_cres.argtypes = [ctypes.POINTER(raw_t),ctypes.c_ubyte]
rtklib.input_cres.restype = ctypes.c_int
def input_cres(raw,data):
  """
input_cres  (raw_t *raw, unsigned char data)"""

  if(type(raw) == raw_t):
    raw = ctypes.byref(raw)

  result = rtklib.input_cres(raw,data)


  return result

rtklib.input_stq.argtypes = [ctypes.POINTER(raw_t),ctypes.c_ubyte]
rtklib.input_stq.restype = ctypes.c_int
def input_stq(raw,data):
  """
input_stq   (raw_t *raw, unsigned char data)"""

  if(type(raw) == raw_t):
    raw = ctypes.byref(raw)

  result = rtklib.input_stq(raw,data)


  return result

rtklib.input_gw10.argtypes = [ctypes.POINTER(raw_t),ctypes.c_ubyte]
rtklib.input_gw10.restype = ctypes.c_int
def input_gw10(raw,data):
  """
input_gw10  (raw_t *raw, unsigned char data)"""

  if(type(raw) == raw_t):
    raw = ctypes.byref(raw)

  result = rtklib.input_gw10(raw,data)


  return result

rtklib.input_javad.argtypes = [ctypes.POINTER(raw_t),ctypes.c_ubyte]
rtklib.input_javad.restype = ctypes.c_int
def input_javad(raw,data):
  """
input_javad (raw_t *raw, unsigned char data)"""

  if(type(raw) == raw_t):
    raw = ctypes.byref(raw)

  result = rtklib.input_javad(raw,data)


  return result

rtklib.input_nvs.argtypes = [ctypes.POINTER(raw_t),ctypes.c_ubyte]
rtklib.input_nvs.restype = ctypes.c_int
def input_nvs(raw,data):
  """
input_nvs   (raw_t *raw, unsigned char data)"""

  if(type(raw) == raw_t):
    raw = ctypes.byref(raw)

  result = rtklib.input_nvs(raw,data)


  return result

rtklib.input_bnx.argtypes = [ctypes.POINTER(raw_t),ctypes.c_ubyte]
rtklib.input_bnx.restype = ctypes.c_int
def input_bnx(raw,data):
  """
input_bnx   (raw_t *raw, unsigned char data)"""

  if(type(raw) == raw_t):
    raw = ctypes.byref(raw)

  result = rtklib.input_bnx(raw,data)


  return result

rtklib.input_rt17.argtypes = [ctypes.POINTER(raw_t),ctypes.c_ubyte]
rtklib.input_rt17.restype = ctypes.c_int
def input_rt17(raw,data):
  """
input_rt17  (raw_t *raw, unsigned char data)"""

  if(type(raw) == raw_t):
    raw = ctypes.byref(raw)

  result = rtklib.input_rt17(raw,data)


  return result

rtklib.input_lexr.argtypes = [ctypes.POINTER(raw_t),ctypes.c_ubyte]
rtklib.input_lexr.restype = ctypes.c_int
def input_lexr(raw,data):
  """
input_lexr  (raw_t *raw, unsigned char data)"""

  if(type(raw) == raw_t):
    raw = ctypes.byref(raw)

  result = rtklib.input_lexr(raw,data)


  return result

rtklib.input_oem4f.argtypes = [ctypes.POINTER(raw_t),ctypes.POINTER(None)]
rtklib.input_oem4f.restype = ctypes.c_int
def input_oem4f(raw,fp):
  """
input_oem4f (raw_t *raw, FILE *fp)"""

  if(type(raw) == raw_t):
    raw = ctypes.byref(raw)

  result = rtklib.input_oem4f(raw,fp)


  return result

rtklib.input_oem3f.argtypes = [ctypes.POINTER(raw_t),ctypes.POINTER(None)]
rtklib.input_oem3f.restype = ctypes.c_int
def input_oem3f(raw,fp):
  """
input_oem3f (raw_t *raw, FILE *fp)"""

  if(type(raw) == raw_t):
    raw = ctypes.byref(raw)

  result = rtklib.input_oem3f(raw,fp)


  return result

rtklib.input_ubxf.argtypes = [ctypes.POINTER(raw_t),ctypes.POINTER(None)]
rtklib.input_ubxf.restype = ctypes.c_int
def input_ubxf(raw,fp):
  """
input_ubxf  (raw_t *raw, FILE *fp)"""

  if(type(raw) == raw_t):
    raw = ctypes.byref(raw)

  result = rtklib.input_ubxf(raw,fp)


  return result

rtklib.input_ss2f.argtypes = [ctypes.POINTER(raw_t),ctypes.POINTER(None)]
rtklib.input_ss2f.restype = ctypes.c_int
def input_ss2f(raw,fp):
  """
input_ss2f  (raw_t *raw, FILE *fp)"""

  if(type(raw) == raw_t):
    raw = ctypes.byref(raw)

  result = rtklib.input_ss2f(raw,fp)


  return result

rtklib.input_cresf.argtypes = [ctypes.POINTER(raw_t),ctypes.POINTER(None)]
rtklib.input_cresf.restype = ctypes.c_int
def input_cresf(raw,fp):
  """
input_cresf (raw_t *raw, FILE *fp)"""

  if(type(raw) == raw_t):
    raw = ctypes.byref(raw)

  result = rtklib.input_cresf(raw,fp)


  return result

rtklib.input_stqf.argtypes = [ctypes.POINTER(raw_t),ctypes.POINTER(None)]
rtklib.input_stqf.restype = ctypes.c_int
def input_stqf(raw,fp):
  """
input_stqf  (raw_t *raw, FILE *fp)"""

  if(type(raw) == raw_t):
    raw = ctypes.byref(raw)

  result = rtklib.input_stqf(raw,fp)


  return result

rtklib.input_gw10f.argtypes = [ctypes.POINTER(raw_t),ctypes.POINTER(None)]
rtklib.input_gw10f.restype = ctypes.c_int
def input_gw10f(raw,fp):
  """
input_gw10f (raw_t *raw, FILE *fp)"""

  if(type(raw) == raw_t):
    raw = ctypes.byref(raw)

  result = rtklib.input_gw10f(raw,fp)


  return result

rtklib.input_javadf.argtypes = [ctypes.POINTER(raw_t),ctypes.POINTER(None)]
rtklib.input_javadf.restype = ctypes.c_int
def input_javadf(raw,fp):
  """
input_javadf(raw_t *raw, FILE *fp)"""

  if(type(raw) == raw_t):
    raw = ctypes.byref(raw)

  result = rtklib.input_javadf(raw,fp)


  return result

rtklib.input_nvsf.argtypes = [ctypes.POINTER(raw_t),ctypes.POINTER(None)]
rtklib.input_nvsf.restype = ctypes.c_int
def input_nvsf(raw,fp):
  """
input_nvsf  (raw_t *raw, FILE *fp)"""

  if(type(raw) == raw_t):
    raw = ctypes.byref(raw)

  result = rtklib.input_nvsf(raw,fp)


  return result

rtklib.input_bnxf.argtypes = [ctypes.POINTER(raw_t),ctypes.POINTER(None)]
rtklib.input_bnxf.restype = ctypes.c_int
def input_bnxf(raw,fp):
  """
input_bnxf  (raw_t *raw, FILE *fp)"""

  if(type(raw) == raw_t):
    raw = ctypes.byref(raw)

  result = rtklib.input_bnxf(raw,fp)


  return result

rtklib.input_rt17f.argtypes = [ctypes.POINTER(raw_t),ctypes.POINTER(None)]
rtklib.input_rt17f.restype = ctypes.c_int
def input_rt17f(raw,fp):
  """
input_rt17f (raw_t *raw, FILE *fp)"""

  if(type(raw) == raw_t):
    raw = ctypes.byref(raw)

  result = rtklib.input_rt17f(raw,fp)


  return result

rtklib.input_lexrf.argtypes = [ctypes.POINTER(raw_t),ctypes.POINTER(None)]
rtklib.input_lexrf.restype = ctypes.c_int
def input_lexrf(raw,fp):
  """
input_lexrf (raw_t *raw, FILE *fp)"""

  if(type(raw) == raw_t):
    raw = ctypes.byref(raw)

  result = rtklib.input_lexrf(raw,fp)


  return result

rtklib.gen_ubx.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.POINTER(ctypes.c_ubyte)]
rtklib.gen_ubx.restype = ctypes.c_int
def gen_ubx(msg,buff):
  """
gen_ubx (const char *msg, unsigned char *buff)"""

  result = rtklib.gen_ubx(msg,buff)


  return result

rtklib.gen_stq.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.POINTER(ctypes.c_ubyte)]
rtklib.gen_stq.restype = ctypes.c_int
def gen_stq(msg,buff):
  """
gen_stq (const char *msg, unsigned char *buff)"""

  result = rtklib.gen_stq(msg,buff)


  return result

rtklib.gen_nvs.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.POINTER(ctypes.c_ubyte)]
rtklib.gen_nvs.restype = ctypes.c_int
def gen_nvs(msg,buff):
  """
gen_nvs (const char *msg, unsigned char *buff)"""

  result = rtklib.gen_nvs(msg,buff)


  return result

rtklib.gen_lexr.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.POINTER(ctypes.c_ubyte)]
rtklib.gen_lexr.restype = ctypes.c_int
def gen_lexr(msg,buff):
  """
gen_lexr(const char *msg, unsigned char *buff)"""

  result = rtklib.gen_lexr(msg,buff)


  return result

rtklib.init_rtcm.argtypes = [ctypes.POINTER(rtcm_t)]
rtklib.init_rtcm.restype = ctypes.c_int
def init_rtcm(rtcm):
  """
init_rtcm   (rtcm_t *rtcm)"""

  if(type(rtcm) == rtcm_t):
    rtcm = ctypes.byref(rtcm)

  result = rtklib.init_rtcm(rtcm)


  return result

rtklib.free_rtcm.argtypes = [ctypes.POINTER(rtcm_t)]
rtklib.free_rtcm.restype = None
def free_rtcm(rtcm):
  """
free_rtcm  (rtcm_t *rtcm)"""

  if(type(rtcm) == rtcm_t):
    rtcm = ctypes.byref(rtcm)

  result = rtklib.free_rtcm(rtcm)


  return result

rtklib.input_rtcm2.argtypes = [ctypes.POINTER(rtcm_t),ctypes.c_ubyte]
rtklib.input_rtcm2.restype = ctypes.c_int
def input_rtcm2(rtcm,data):
  """
input_rtcm2 (rtcm_t *rtcm, unsigned char data)"""

  if(type(rtcm) == rtcm_t):
    rtcm = ctypes.byref(rtcm)

  result = rtklib.input_rtcm2(rtcm,data)


  return result

rtklib.input_rtcm3.argtypes = [ctypes.POINTER(rtcm_t),ctypes.c_ubyte]
rtklib.input_rtcm3.restype = ctypes.c_int
def input_rtcm3(rtcm,data):
  """
input_rtcm3 (rtcm_t *rtcm, unsigned char data)"""

  if(type(rtcm) == rtcm_t):
    rtcm = ctypes.byref(rtcm)

  result = rtklib.input_rtcm3(rtcm,data)


  return result

rtklib.input_rtcm2f.argtypes = [ctypes.POINTER(rtcm_t),ctypes.POINTER(None)]
rtklib.input_rtcm2f.restype = ctypes.c_int
def input_rtcm2f(rtcm,fp):
  """
input_rtcm2f(rtcm_t *rtcm, FILE *fp)"""

  if(type(rtcm) == rtcm_t):
    rtcm = ctypes.byref(rtcm)

  result = rtklib.input_rtcm2f(rtcm,fp)


  return result

rtklib.input_rtcm3f.argtypes = [ctypes.POINTER(rtcm_t),ctypes.POINTER(None)]
rtklib.input_rtcm3f.restype = ctypes.c_int
def input_rtcm3f(rtcm,fp):
  """
input_rtcm3f(rtcm_t *rtcm, FILE *fp)"""

  if(type(rtcm) == rtcm_t):
    rtcm = ctypes.byref(rtcm)

  result = rtklib.input_rtcm3f(rtcm,fp)


  return result

rtklib.gen_rtcm2.argtypes = [ctypes.POINTER(rtcm_t),ctypes.c_int,ctypes.c_int]
rtklib.gen_rtcm2.restype = ctypes.c_int
def gen_rtcm2(rtcm,type,sync):
  """
gen_rtcm2   (rtcm_t *rtcm, int type, int sync)"""

  if(type(rtcm) == rtcm_t):
    rtcm = ctypes.byref(rtcm)

  result = rtklib.gen_rtcm2(rtcm,type,sync)


  return result

rtklib.gen_rtcm3.argtypes = [ctypes.POINTER(rtcm_t),ctypes.c_int,ctypes.c_int]
rtklib.gen_rtcm3.restype = ctypes.c_int
def gen_rtcm3(rtcm,type,sync):
  """
gen_rtcm3   (rtcm_t *rtcm, int type, int sync)"""

  if(type(rtcm) == rtcm_t):
    rtcm = ctypes.byref(rtcm)

  result = rtklib.gen_rtcm3(rtcm,type,sync)


  return result

rtklib.initsolbuf.argtypes = [ctypes.POINTER(solbuf_t),ctypes.c_int,ctypes.c_int]
rtklib.initsolbuf.restype = None
def initsolbuf(solbuf,cyclic,nmax):
  """
initsolbuf(solbuf_t *solbuf, int cyclic, int nmax)"""

  if(type(solbuf) == solbuf_t):
    solbuf = ctypes.byref(solbuf)

  result = rtklib.initsolbuf(solbuf,cyclic,nmax)


  return result

rtklib.freesolbuf.argtypes = [ctypes.POINTER(solbuf_t)]
rtklib.freesolbuf.restype = None
def freesolbuf(solbuf):
  """
freesolbuf(solbuf_t *solbuf)"""

  if(type(solbuf) == solbuf_t):
    solbuf = ctypes.byref(solbuf)

  result = rtklib.freesolbuf(solbuf)


  return result

rtklib.freesolstatbuf.argtypes = [ctypes.POINTER(solstatbuf_t)]
rtklib.freesolstatbuf.restype = None
def freesolstatbuf(solstatbuf):
  """
freesolstatbuf(solstatbuf_t *solstatbuf)"""

  if(type(solstatbuf) == solstatbuf_t):
    solstatbuf = ctypes.byref(solstatbuf)

  result = rtklib.freesolstatbuf(solstatbuf)


  return result

rtklib.getsol.argtypes = [ctypes.POINTER(solbuf_t),ctypes.c_int]
rtklib.getsol.restype = ctypes.POINTER(sol_t)
def getsol(solbuf,index):
  """
getsol(solbuf_t *solbuf, int index)"""

  if(type(solbuf) == solbuf_t):
    solbuf = ctypes.byref(solbuf)

  result = rtklib.getsol(solbuf,index)


  return result

rtklib.addsol.argtypes = [ctypes.POINTER(solbuf_t),ctypes.POINTER(sol_t)]
rtklib.addsol.restype = ctypes.c_int
def addsol(solbuf,sol):
  """
addsol(solbuf_t *solbuf, const sol_t *sol)"""

  if(type(solbuf) == solbuf_t):
    solbuf = ctypes.byref(solbuf)

  if(type(sol) == sol_t):
    sol = ctypes.byref(sol)

  result = rtklib.addsol(solbuf,sol)


  return result

rtklib.inputsol.argtypes = [ctypes.c_ubyte,gtime_t,gtime_t,ctypes.c_double,ctypes.c_int,ctypes.POINTER(solopt_t),ctypes.POINTER(solbuf_t)]
rtklib.inputsol.restype = ctypes.c_int
def inputsol(data,ts,te,tint,qflag,opt,solbuf):
  """
inputsol(unsigned char data, gtime_t ts, gtime_t te, double tint,
                    int qflag, const solopt_t *opt, solbuf_t *solbuf)"""

  if(type(opt) == solopt_t):
    opt = ctypes.byref(opt)

  if(type(solbuf) == solbuf_t):
    solbuf = ctypes.byref(solbuf)

  result = rtklib.inputsol(data,ts,te,tint,qflag,opt,solbuf)


  return result

rtklib.outprcopts.argtypes = [ctypes.POINTER(ctypes.c_ubyte),ctypes.POINTER(prcopt_t)]
rtklib.outprcopts.restype = ctypes.c_int
def outprcopts(buff,opt):
  """
outprcopts(unsigned char *buff, const prcopt_t *opt)"""

  if(type(opt) == prcopt_t):
    opt = ctypes.byref(opt)

  result = rtklib.outprcopts(buff,opt)


  return result

rtklib.outsolheads.argtypes = [ctypes.POINTER(ctypes.c_ubyte),ctypes.POINTER(solopt_t)]
rtklib.outsolheads.restype = ctypes.c_int
def outsolheads(buff,opt):
  """
outsolheads(unsigned char *buff, const solopt_t *opt)"""

  if(type(opt) == solopt_t):
    opt = ctypes.byref(opt)

  result = rtklib.outsolheads(buff,opt)


  return result

rtklib.outsols.argtypes = [ctypes.POINTER(ctypes.c_ubyte),ctypes.POINTER(sol_t),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(solopt_t)]
rtklib.outsols.restype = ctypes.c_int
def outsols(buff,sol,rb,opt):
  """
outsols  (unsigned char *buff, const sol_t *sol, const double *rb,
                     const solopt_t *opt)"""

  if(type(sol) == sol_t):
    sol = ctypes.byref(sol)

  if(type(opt) == solopt_t):
    opt = ctypes.byref(opt)

  result = rtklib.outsols(buff,sol,rb,opt)


  return result

rtklib.outsolexs.argtypes = [ctypes.POINTER(ctypes.c_ubyte),ctypes.POINTER(sol_t),ctypes.POINTER(ssat_t),ctypes.POINTER(solopt_t)]
rtklib.outsolexs.restype = ctypes.c_int
def outsolexs(buff,sol,ssat,opt):
  """
outsolexs(unsigned char *buff, const sol_t *sol, const ssat_t *ssat,
                     const solopt_t *opt)"""

  if(type(sol) == sol_t):
    sol = ctypes.byref(sol)

  if(type(ssat) == ssat_t):
    ssat = ctypes.byref(ssat)

  if(type(opt) == solopt_t):
    opt = ctypes.byref(opt)

  result = rtklib.outsolexs(buff,sol,ssat,opt)


  return result

rtklib.outnmea_rmc.argtypes = [ctypes.POINTER(ctypes.c_ubyte),ctypes.POINTER(sol_t)]
rtklib.outnmea_rmc.restype = ctypes.c_int
def outnmea_rmc(buff,sol):
  """
outnmea_rmc(unsigned char *buff, const sol_t *sol)"""

  if(type(sol) == sol_t):
    sol = ctypes.byref(sol)

  result = rtklib.outnmea_rmc(buff,sol)


  return result

rtklib.outnmea_gga.argtypes = [ctypes.POINTER(ctypes.c_ubyte),ctypes.POINTER(sol_t)]
rtklib.outnmea_gga.restype = ctypes.c_int
def outnmea_gga(buff,sol):
  """
outnmea_gga(unsigned char *buff, const sol_t *sol)"""

  if(type(sol) == sol_t):
    sol = ctypes.byref(sol)

  result = rtklib.outnmea_gga(buff,sol)


  return result

rtklib.outnmea_gsa.argtypes = [ctypes.POINTER(ctypes.c_ubyte),ctypes.POINTER(sol_t),ctypes.POINTER(ssat_t)]
rtklib.outnmea_gsa.restype = ctypes.c_int
def outnmea_gsa(buff,sol,ssat):
  """
outnmea_gsa(unsigned char *buff, const sol_t *sol,
                       const ssat_t *ssat)"""

  if(type(sol) == sol_t):
    sol = ctypes.byref(sol)

  if(type(ssat) == ssat_t):
    ssat = ctypes.byref(ssat)

  result = rtklib.outnmea_gsa(buff,sol,ssat)


  return result

rtklib.outnmea_gsv.argtypes = [ctypes.POINTER(ctypes.c_ubyte),ctypes.POINTER(sol_t),ctypes.POINTER(ssat_t)]
rtklib.outnmea_gsv.restype = ctypes.c_int
def outnmea_gsv(buff,sol,ssat):
  """
outnmea_gsv(unsigned char *buff, const sol_t *sol,
                       const ssat_t *ssat)"""

  if(type(sol) == sol_t):
    sol = ctypes.byref(sol)

  if(type(ssat) == ssat_t):
    ssat = ctypes.byref(ssat)

  result = rtklib.outnmea_gsv(buff,sol,ssat)


  return result

rtklib.convkml.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.POINTER(ctypes.c_char),gtime_t,gtime_t,ctypes.c_double,ctypes.c_int,ctypes.POINTER(ctypes.c_double),ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int]
rtklib.convkml.restype = ctypes.c_int
def convkml(infile,outfile,ts,te,tint,qflg,offset,tcolor,pcolor,outalt,outtime):
  """
convkml(const char *infile, const char *outfile, gtime_t ts,
                   gtime_t te, double tint, int qflg, double *offset,
                   int tcolor, int pcolor, int outalt, int outtime)"""

  result = rtklib.convkml(infile,outfile,ts,te,tint,qflg,offset,tcolor,pcolor,outalt,outtime)


  return result

rtklib.sbsreadmsg.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.c_int,ctypes.POINTER(sbs_t)]
rtklib.sbsreadmsg.restype = ctypes.c_int
def sbsreadmsg(file,sel,sbs):
  """
sbsreadmsg (const char *file, int sel, sbs_t *sbs)"""

  if(type(sbs) == sbs_t):
    sbs = ctypes.byref(sbs)

  result = rtklib.sbsreadmsg(file,sel,sbs)


  return result

rtklib.sbsreadmsgt.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.c_int,gtime_t,gtime_t,ctypes.POINTER(sbs_t)]
rtklib.sbsreadmsgt.restype = ctypes.c_int
def sbsreadmsgt(file,sel,ts,te,sbs):
  """
sbsreadmsgt(const char *file, int sel, gtime_t ts, gtime_t te,
                        sbs_t *sbs)"""

  if(type(sbs) == sbs_t):
    sbs = ctypes.byref(sbs)

  result = rtklib.sbsreadmsgt(file,sel,ts,te,sbs)


  return result

rtklib.sbsdecodemsg.argtypes = [gtime_t,ctypes.c_int,ctypes.POINTER(ctypes.c_uint),ctypes.POINTER(sbsmsg_t)]
rtklib.sbsdecodemsg.restype = ctypes.c_int
def sbsdecodemsg(time,prn,words,sbsmsg):
  """
sbsdecodemsg(gtime_t time, int prn, const unsigned int *words,
                         sbsmsg_t *sbsmsg)"""

  if(type(sbsmsg) == sbsmsg_t):
    sbsmsg = ctypes.byref(sbsmsg)

  result = rtklib.sbsdecodemsg(time,prn,words,sbsmsg)


  return result

rtklib.sbsupdatecorr.argtypes = [ctypes.POINTER(sbsmsg_t),ctypes.POINTER(nav_t)]
rtklib.sbsupdatecorr.restype = ctypes.c_int
def sbsupdatecorr(msg,nav):
  """
sbsupdatecorr(const sbsmsg_t *msg, nav_t *nav)"""

  if(type(msg) == sbsmsg_t):
    msg = ctypes.byref(msg)

  if(type(nav) == nav_t):
    nav = ctypes.byref(nav)

  result = rtklib.sbsupdatecorr(msg,nav)


  return result

rtklib.sbssatcorr.argtypes = [gtime_t,ctypes.c_int,ctypes.POINTER(nav_t),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
rtklib.sbssatcorr.restype = ctypes.c_int
def sbssatcorr(time,sat,nav,rs,dts,var):
  """
sbssatcorr(gtime_t time, int sat, const nav_t *nav, double *rs,
                      double *dts, double *var)"""

  if(type(nav) == nav_t):
    nav = ctypes.byref(nav)

  result = rtklib.sbssatcorr(time,sat,nav,rs,dts,var)


  return result

rtklib.sbsioncorr.argtypes = [gtime_t,ctypes.POINTER(nav_t),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
rtklib.sbsioncorr.restype = ctypes.c_int
def sbsioncorr(time,nav,pos,azel,delay,var):
  """
sbsioncorr(gtime_t time, const nav_t *nav, const double *pos,
                      const double *azel, double *delay, double *var)"""

  if(type(nav) == nav_t):
    nav = ctypes.byref(nav)

  result = rtklib.sbsioncorr(time,nav,pos,azel,delay,var)


  return result

rtklib.sbstropcorr.argtypes = [gtime_t,ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
rtklib.sbstropcorr.restype = ctypes.c_double
def sbstropcorr(time,pos,azel,var):
  """
sbstropcorr(gtime_t time, const double *pos, const double *azel,
                          double *var)"""

  result = rtklib.sbstropcorr(time,pos,azel,var)


  return result

rtklib.searchopt.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.POINTER(opt_t)]
rtklib.searchopt.restype = ctypes.POINTER(opt_t)
def searchopt(name,opts):
  """
searchopt(const char *name, const opt_t *opts)"""

  if(type(opts) == opt_t):
    opts = ctypes.byref(opts)

  result = rtklib.searchopt(name,opts)


  return result

rtklib.str2opt.argtypes = [ctypes.POINTER(opt_t),ctypes.POINTER(ctypes.c_char)]
rtklib.str2opt.restype = ctypes.c_int
def str2opt(opt,str):
  """
str2opt(opt_t *opt, const char *str)"""

  if(type(opt) == opt_t):
    opt = ctypes.byref(opt)

  result = rtklib.str2opt(opt,str)


  return result

rtklib.opt2str.argtypes = [ctypes.POINTER(opt_t),ctypes.POINTER(ctypes.c_char)]
rtklib.opt2str.restype = ctypes.c_int
def opt2str(opt,str):
  """
opt2str(const opt_t *opt, char *str)"""

  if(type(opt) == opt_t):
    opt = ctypes.byref(opt)

  result = rtklib.opt2str(opt,str)


  return result

rtklib.opt2buf.argtypes = [ctypes.POINTER(opt_t),ctypes.POINTER(ctypes.c_char)]
rtklib.opt2buf.restype = ctypes.c_int
def opt2buf(opt,buff):
  """
opt2buf(const opt_t *opt, char *buff)"""

  if(type(opt) == opt_t):
    opt = ctypes.byref(opt)

  result = rtklib.opt2buf(opt,buff)


  return result

rtklib.loadopts.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.POINTER(opt_t)]
rtklib.loadopts.restype = ctypes.c_int
def loadopts(file,opts):
  """
loadopts(const char *file, opt_t *opts)"""

  if(type(opts) == opt_t):
    opts = ctypes.byref(opts)

  result = rtklib.loadopts(file,opts)


  return result

rtklib.saveopts.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.POINTER(ctypes.c_char),ctypes.POINTER(ctypes.c_char),ctypes.POINTER(opt_t)]
rtklib.saveopts.restype = ctypes.c_int
def saveopts(file,mode,comment,opts):
  """
saveopts(const char *file, const char *mode, const char *comment,
                    const opt_t *opts)"""

  if(type(opts) == opt_t):
    opts = ctypes.byref(opts)

  result = rtklib.saveopts(file,mode,comment,opts)


  return result

rtklib.resetsysopts.argtypes = []
rtklib.resetsysopts.restype = None
def resetsysopts():
  """
resetsysopts(void)"""

  result = rtklib.resetsysopts()


  return result

rtklib.getsysopts.argtypes = [ctypes.POINTER(prcopt_t),ctypes.POINTER(solopt_t),ctypes.POINTER(filopt_t)]
rtklib.getsysopts.restype = None
def getsysopts(popt,sopt,fopt):
  """
getsysopts(prcopt_t *popt, solopt_t *sopt, filopt_t *fopt)"""

  if(type(popt) == prcopt_t):
    popt = ctypes.byref(popt)

  if(type(sopt) == solopt_t):
    sopt = ctypes.byref(sopt)

  if(type(fopt) == filopt_t):
    fopt = ctypes.byref(fopt)

  result = rtklib.getsysopts(popt,sopt,fopt)


  return result

rtklib.setsysopts.argtypes = [ctypes.POINTER(prcopt_t),ctypes.POINTER(solopt_t),ctypes.POINTER(filopt_t)]
rtklib.setsysopts.restype = None
def setsysopts(popt,sopt,fopt):
  """
setsysopts(const prcopt_t *popt, const solopt_t *sopt,
                       const filopt_t *fopt)"""

  if(type(popt) == prcopt_t):
    popt = ctypes.byref(popt)

  if(type(sopt) == solopt_t):
    sopt = ctypes.byref(sopt)

  if(type(fopt) == filopt_t):
    fopt = ctypes.byref(fopt)

  result = rtklib.setsysopts(popt,sopt,fopt)


  return result

rtklib.strinitcom.argtypes = []
rtklib.strinitcom.restype = None
def strinitcom():
  """
strinitcom(void)"""

  result = rtklib.strinitcom()


  return result

rtklib.strinit.argtypes = [ctypes.POINTER(stream_t)]
rtklib.strinit.restype = None
def strinit(stream):
  """
strinit  (stream_t *stream)"""

  if(type(stream) == stream_t):
    stream = ctypes.byref(stream)

  result = rtklib.strinit(stream)


  return result

rtklib.strlock.argtypes = [ctypes.POINTER(stream_t)]
rtklib.strlock.restype = None
def strlock(stream):
  """
strlock  (stream_t *stream)"""

  if(type(stream) == stream_t):
    stream = ctypes.byref(stream)

  result = rtklib.strlock(stream)


  return result

rtklib.strunlock.argtypes = [ctypes.POINTER(stream_t)]
rtklib.strunlock.restype = None
def strunlock(stream):
  """
strunlock(stream_t *stream)"""

  if(type(stream) == stream_t):
    stream = ctypes.byref(stream)

  result = rtklib.strunlock(stream)


  return result

rtklib.stropen.argtypes = [ctypes.POINTER(stream_t),ctypes.c_int,ctypes.c_int,ctypes.POINTER(ctypes.c_char)]
rtklib.stropen.restype = ctypes.c_int
def stropen(stream,type,mode,path):
  """
stropen  (stream_t *stream, int type, int mode, const char *path)"""

  if(type(stream) == stream_t):
    stream = ctypes.byref(stream)

  result = rtklib.stropen(stream,type,mode,path)


  return result

rtklib.strclose.argtypes = [ctypes.POINTER(stream_t)]
rtklib.strclose.restype = None
def strclose(stream):
  """
strclose (stream_t *stream)"""

  if(type(stream) == stream_t):
    stream = ctypes.byref(stream)

  result = rtklib.strclose(stream)


  return result

rtklib.strread.argtypes = [ctypes.POINTER(stream_t),ctypes.POINTER(ctypes.c_ubyte),ctypes.c_int]
rtklib.strread.restype = ctypes.c_int
def strread(stream,buff,n):
  """
strread  (stream_t *stream, unsigned char *buff, int n)"""

  if(type(stream) == stream_t):
    stream = ctypes.byref(stream)

  result = rtklib.strread(stream,buff,n)


  return result

rtklib.strwrite.argtypes = [ctypes.POINTER(stream_t),ctypes.POINTER(ctypes.c_ubyte),ctypes.c_int]
rtklib.strwrite.restype = ctypes.c_int
def strwrite(stream,buff,n):
  """
strwrite (stream_t *stream, unsigned char *buff, int n)"""

  if(type(stream) == stream_t):
    stream = ctypes.byref(stream)

  result = rtklib.strwrite(stream,buff,n)


  return result

rtklib.strsync.argtypes = [ctypes.POINTER(stream_t),ctypes.POINTER(stream_t)]
rtklib.strsync.restype = None
def strsync(stream1,stream2):
  """
strsync  (stream_t *stream1, stream_t *stream2)"""

  if(type(stream1) == stream_t):
    stream1 = ctypes.byref(stream1)

  if(type(stream2) == stream_t):
    stream2 = ctypes.byref(stream2)

  result = rtklib.strsync(stream1,stream2)


  return result

rtklib.strstat.argtypes = [ctypes.POINTER(stream_t),ctypes.POINTER(ctypes.c_char)]
rtklib.strstat.restype = ctypes.c_int
def strstat(stream,msg):
  """
strstat  (stream_t *stream, char *msg)"""

  if(type(stream) == stream_t):
    stream = ctypes.byref(stream)

  result = rtklib.strstat(stream,msg)


  return result

rtklib.strsum.argtypes = [ctypes.POINTER(stream_t),ctypes.POINTER(ctypes.c_int),ctypes.POINTER(ctypes.c_int),ctypes.POINTER(ctypes.c_int),ctypes.POINTER(ctypes.c_int)]
rtklib.strsum.restype = None
def strsum(stream,inb,inr,outb,outr):
  """
strsum   (stream_t *stream, int *inb, int *inr, int *outb, int *outr)"""

  if(type(stream) == stream_t):
    stream = ctypes.byref(stream)

  result = rtklib.strsum(stream,inb,inr,outb,outr)


  return result

rtklib.strsetopt.argtypes = [ctypes.POINTER(ctypes.c_int)]
rtklib.strsetopt.restype = None
def strsetopt(opt):
  """
strsetopt(const int *opt)"""

  result = rtklib.strsetopt(opt)


  return result

rtklib.strgettime.argtypes = [ctypes.POINTER(stream_t)]
rtklib.strgettime.restype = gtime_t
def strgettime(stream):
  """
strgettime(stream_t *stream)"""

  if(type(stream) == stream_t):
    stream = ctypes.byref(stream)

  result = rtklib.strgettime(stream)


  return result

rtklib.strsendnmea.argtypes = [ctypes.POINTER(stream_t),ctypes.POINTER(ctypes.c_double)]
rtklib.strsendnmea.restype = None
def strsendnmea(stream,pos):
  """
strsendnmea(stream_t *stream, const double *pos)"""

  if(type(stream) == stream_t):
    stream = ctypes.byref(stream)

  result = rtklib.strsendnmea(stream,pos)


  return result

rtklib.strsendcmd.argtypes = [ctypes.POINTER(stream_t),ctypes.POINTER(ctypes.c_char)]
rtklib.strsendcmd.restype = None
def strsendcmd(stream,cmd):
  """
strsendcmd(stream_t *stream, const char *cmd)"""

  if(type(stream) == stream_t):
    stream = ctypes.byref(stream)

  result = rtklib.strsendcmd(stream,cmd)


  return result

rtklib.strsettimeout.argtypes = [ctypes.POINTER(stream_t),ctypes.c_int,ctypes.c_int]
rtklib.strsettimeout.restype = None
def strsettimeout(stream,toinact,tirecon):
  """
strsettimeout(stream_t *stream, int toinact, int tirecon)"""

  if(type(stream) == stream_t):
    stream = ctypes.byref(stream)

  result = rtklib.strsettimeout(stream,toinact,tirecon)


  return result

rtklib.strsetdir.argtypes = [ctypes.POINTER(ctypes.c_char)]
rtklib.strsetdir.restype = None
def strsetdir(dir):
  """
strsetdir(const char *dir)"""

  result = rtklib.strsetdir(dir)


  return result

rtklib.strsetproxy.argtypes = [ctypes.POINTER(ctypes.c_char)]
rtklib.strsetproxy.restype = None
def strsetproxy(addr):
  """
strsetproxy(const char *addr)"""

  result = rtklib.strsetproxy(addr)


  return result

rtklib.pntpos.argtypes = [ctypes.POINTER(obsd_t),ctypes.c_int,ctypes.POINTER(nav_t),ctypes.POINTER(prcopt_t),ctypes.POINTER(sol_t),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ssat_t),ctypes.POINTER(ctypes.c_char)]
rtklib.pntpos.restype = ctypes.c_int
def pntpos(obs,n,nav,opt,sol,azel,ssat,msg):
  """
pntpos(const obsd_t *obs, int n, const nav_t *nav,
                  const prcopt_t *opt, sol_t *sol, double *azel,
                  ssat_t *ssat, char *msg)"""

  if(type(obs) == obsd_t):
    obs = ctypes.byref(obs)

  if(type(nav) == nav_t):
    nav = ctypes.byref(nav)

  if(type(opt) == prcopt_t):
    opt = ctypes.byref(opt)

  if(type(sol) == sol_t):
    sol = ctypes.byref(sol)

  if(type(ssat) == ssat_t):
    ssat = ctypes.byref(ssat)

  result = rtklib.pntpos(obs,n,nav,opt,sol,azel,ssat,msg)


  return result

rtklib.rtkinit.argtypes = [ctypes.POINTER(rtk_t),ctypes.POINTER(prcopt_t)]
rtklib.rtkinit.restype = None
def rtkinit(rtk,opt):
  """
rtkinit(rtk_t *rtk, const prcopt_t *opt)"""

  if(type(rtk) == rtk_t):
    rtk = ctypes.byref(rtk)

  if(type(opt) == prcopt_t):
    opt = ctypes.byref(opt)

  result = rtklib.rtkinit(rtk,opt)


  return result

rtklib.rtkfree.argtypes = [ctypes.POINTER(rtk_t)]
rtklib.rtkfree.restype = None
def rtkfree(rtk):
  """
rtkfree(rtk_t *rtk)"""

  if(type(rtk) == rtk_t):
    rtk = ctypes.byref(rtk)

  result = rtklib.rtkfree(rtk)


  return result

rtklib.rtkpos.argtypes = [ctypes.POINTER(rtk_t),ctypes.POINTER(obsd_t),ctypes.c_int,ctypes.POINTER(nav_t)]
rtklib.rtkpos.restype = ctypes.c_int
def rtkpos(rtk,obs,nobs,nav):
  """
rtkpos (rtk_t *rtk, const obsd_t *obs, int nobs, const nav_t *nav)"""

  if(type(rtk) == rtk_t):
    rtk = ctypes.byref(rtk)

  if(type(obs) == obsd_t):
    obs = ctypes.byref(obs)

  if(type(nav) == nav_t):
    nav = ctypes.byref(nav)

  result = rtklib.rtkpos(rtk,obs,nobs,nav)


  return result

rtklib.rtkopenstat.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.c_int]
rtklib.rtkopenstat.restype = ctypes.c_int
def rtkopenstat(file,level):
  """
rtkopenstat(const char *file, int level)"""

  result = rtklib.rtkopenstat(file,level)


  return result

rtklib.rtkclosestat.argtypes = []
rtklib.rtkclosestat.restype = None
def rtkclosestat():
  """
rtkclosestat(void)"""

  result = rtklib.rtkclosestat()


  return result

rtklib.pppos.argtypes = [ctypes.POINTER(rtk_t),ctypes.POINTER(obsd_t),ctypes.c_int,ctypes.POINTER(nav_t)]
rtklib.pppos.restype = None
def pppos(rtk,obs,n,nav):
  """
pppos(rtk_t *rtk, const obsd_t *obs, int n, const nav_t *nav)"""

  if(type(rtk) == rtk_t):
    rtk = ctypes.byref(rtk)

  if(type(obs) == obsd_t):
    obs = ctypes.byref(obs)

  if(type(nav) == nav_t):
    nav = ctypes.byref(nav)

  result = rtklib.pppos(rtk,obs,n,nav)


  return result

rtklib.pppamb.argtypes = [ctypes.POINTER(rtk_t),ctypes.POINTER(obsd_t),ctypes.c_int,ctypes.POINTER(nav_t),ctypes.POINTER(ctypes.c_double)]
rtklib.pppamb.restype = ctypes.c_int
def pppamb(rtk,obs,n,nav,azel):
  """
pppamb(rtk_t *rtk, const obsd_t *obs, int n, const nav_t *nav,
                  const double *azel)"""

  if(type(rtk) == rtk_t):
    rtk = ctypes.byref(rtk)

  if(type(obs) == obsd_t):
    obs = ctypes.byref(obs)

  if(type(nav) == nav_t):
    nav = ctypes.byref(nav)

  result = rtklib.pppamb(rtk,obs,n,nav,azel)


  return result

rtklib.pppnx.argtypes = [ctypes.POINTER(prcopt_t)]
rtklib.pppnx.restype = ctypes.c_int
def pppnx(opt):
  """
pppnx(const prcopt_t *opt)"""

  if(type(opt) == prcopt_t):
    opt = ctypes.byref(opt)

  result = rtklib.pppnx(opt)


  return result

rtklib.windupcorr.argtypes = [gtime_t,ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
rtklib.windupcorr.restype = None
def windupcorr(time,rs,rr,phw):
  """
windupcorr(gtime_t time, const double *rs, const double *rr,
                       double *phw)"""

  result = rtklib.windupcorr(time,rs,rr,phw)


  return result

rtklib.postpos.argtypes = [gtime_t,gtime_t,ctypes.c_double,ctypes.c_double,ctypes.POINTER(prcopt_t),ctypes.POINTER(solopt_t),ctypes.POINTER(filopt_t),ctypes.POINTER(ctypes.c_void_p),ctypes.c_int,ctypes.POINTER(ctypes.c_char),ctypes.POINTER(ctypes.c_char),ctypes.POINTER(ctypes.c_char)]
rtklib.postpos.restype = ctypes.c_int
def postpos(ts,te,ti,tu,popt,sopt,fopt,infile,n,outfile,rov,base):
  """
postpos(gtime_t ts, gtime_t te, double ti, double tu,
                   const prcopt_t *popt, const solopt_t *sopt,
                   const filopt_t *fopt, char **infile, int n, char *outfile,
                   const char *rov, const char *base)"""

  if(type(popt) == prcopt_t):
    popt = ctypes.byref(popt)

  if(type(sopt) == solopt_t):
    sopt = ctypes.byref(sopt)

  if(type(fopt) == filopt_t):
    fopt = ctypes.byref(fopt)

  result = rtklib.postpos(ts,te,ti,tu,popt,sopt,fopt,infile,n,outfile,rov,base)


  return result

rtklib.strsvrinit.argtypes = [ctypes.POINTER(strsvr_t),ctypes.c_int]
rtklib.strsvrinit.restype = None
def strsvrinit(svr,nout):
  """
strsvrinit (strsvr_t *svr, int nout)"""

  if(type(svr) == strsvr_t):
    svr = ctypes.byref(svr)

  result = rtklib.strsvrinit(svr,nout)


  return result

rtklib.strsvrstart.argtypes = [ctypes.POINTER(strsvr_t),ctypes.POINTER(ctypes.c_int),ctypes.POINTER(ctypes.c_int),ctypes.POINTER(ctypes.c_void_p),ctypes.POINTER(ctypes.c_void_p),ctypes.POINTER(ctypes.c_char),ctypes.POINTER(ctypes.c_double)]
rtklib.strsvrstart.restype = ctypes.c_int
def strsvrstart(svr,opts,strs,paths,conv,cmd,nmeapos):
  """
strsvrstart(strsvr_t *svr, int *opts, int *strs, char **paths,
                        strconv_t **conv, const char *cmd,
                        const double *nmeapos)"""

  if(type(svr) == strsvr_t):
    svr = ctypes.byref(svr)

  result = rtklib.strsvrstart(svr,opts,strs,paths,conv,cmd,nmeapos)


  return result

rtklib.strsvrstop.argtypes = [ctypes.POINTER(strsvr_t),ctypes.POINTER(ctypes.c_char)]
rtklib.strsvrstop.restype = None
def strsvrstop(svr,cmd):
  """
strsvrstop (strsvr_t *svr, const char *cmd)"""

  if(type(svr) == strsvr_t):
    svr = ctypes.byref(svr)

  result = rtklib.strsvrstop(svr,cmd)


  return result

rtklib.strsvrstat.argtypes = [ctypes.POINTER(strsvr_t),ctypes.POINTER(ctypes.c_int),ctypes.POINTER(ctypes.c_int),ctypes.POINTER(ctypes.c_int),ctypes.POINTER(ctypes.c_char)]
rtklib.strsvrstat.restype = None
def strsvrstat(svr,stat,byte,bps,msg):
  """
strsvrstat (strsvr_t *svr, int *stat, int *byte, int *bps, char *msg)"""

  if(type(svr) == strsvr_t):
    svr = ctypes.byref(svr)

  result = rtklib.strsvrstat(svr,stat,byte,bps,msg)


  return result

rtklib.strconvnew.argtypes = [ctypes.c_int,ctypes.c_int,ctypes.POINTER(ctypes.c_char),ctypes.c_int,ctypes.c_int,ctypes.POINTER(ctypes.c_char)]
rtklib.strconvnew.restype = ctypes.POINTER(strconv_t)
def strconvnew(itype,otype,msgs,staid,stasel,opt):
  """
strconvnew(int itype, int otype, const char *msgs, int staid,
                             int stasel, const char *opt)"""

  result = rtklib.strconvnew(itype,otype,msgs,staid,stasel,opt)


  return result

rtklib.strconvfree.argtypes = [ctypes.POINTER(strconv_t)]
rtklib.strconvfree.restype = None
def strconvfree(conv):
  """
strconvfree(strconv_t *conv)"""

  if(type(conv) == strconv_t):
    conv = ctypes.byref(conv)

  result = rtklib.strconvfree(conv)


  return result

rtklib.rtksvrinit.argtypes = [ctypes.POINTER(rtksvr_t)]
rtklib.rtksvrinit.restype = ctypes.c_int
def rtksvrinit(svr):
  """
rtksvrinit  (rtksvr_t *svr)"""

  if(type(svr) == rtksvr_t):
    svr = ctypes.byref(svr)

  result = rtklib.rtksvrinit(svr)


  return result

rtklib.rtksvrfree.argtypes = [ctypes.POINTER(rtksvr_t)]
rtklib.rtksvrfree.restype = None
def rtksvrfree(svr):
  """
rtksvrfree  (rtksvr_t *svr)"""

  if(type(svr) == rtksvr_t):
    svr = ctypes.byref(svr)

  result = rtklib.rtksvrfree(svr)


  return result

rtklib.rtksvrstart.argtypes = [ctypes.POINTER(rtksvr_t),ctypes.c_int,ctypes.c_int,ctypes.POINTER(ctypes.c_int),ctypes.POINTER(ctypes.c_void_p),ctypes.POINTER(ctypes.c_int),ctypes.c_int,ctypes.POINTER(ctypes.c_void_p),ctypes.POINTER(ctypes.c_void_p),ctypes.c_int,ctypes.c_int,ctypes.POINTER(ctypes.c_double),ctypes.POINTER(prcopt_t),ctypes.POINTER(solopt_t),ctypes.POINTER(stream_t)]
rtklib.rtksvrstart.restype = ctypes.c_int
def rtksvrstart(svr,cycle,buffsize,strs,paths,formats,navsel,cmds,rcvopts,nmeacycle,nmeareq,nmeapos,prcopt,solopt,moni):
  """
rtksvrstart (rtksvr_t *svr, int cycle, int buffsize, int *strs,
                         char **paths, int *formats, int navsel, char **cmds,
                         char **rcvopts, int nmeacycle, int nmeareq,
                         const double *nmeapos, prcopt_t *prcopt,
                         solopt_t *solopt, stream_t *moni)"""

  if(type(svr) == rtksvr_t):
    svr = ctypes.byref(svr)

  if(type(prcopt) == prcopt_t):
    prcopt = ctypes.byref(prcopt)

  if(type(solopt) == solopt_t):
    solopt = ctypes.byref(solopt)

  if(type(moni) == stream_t):
    moni = ctypes.byref(moni)

  result = rtklib.rtksvrstart(svr,cycle,buffsize,strs,paths,formats,navsel,cmds,rcvopts,nmeacycle,nmeareq,nmeapos,prcopt,solopt,moni)


  return result

rtklib.rtksvrstop.argtypes = [ctypes.POINTER(rtksvr_t),ctypes.POINTER(ctypes.c_void_p)]
rtklib.rtksvrstop.restype = None
def rtksvrstop(svr,cmds):
  """
rtksvrstop  (rtksvr_t *svr, char **cmds)"""

  if(type(svr) == rtksvr_t):
    svr = ctypes.byref(svr)

  result = rtklib.rtksvrstop(svr,cmds)


  return result

rtklib.rtksvropenstr.argtypes = [ctypes.POINTER(rtksvr_t),ctypes.c_int,ctypes.c_int,ctypes.POINTER(ctypes.c_char),ctypes.POINTER(solopt_t)]
rtklib.rtksvropenstr.restype = ctypes.c_int
def rtksvropenstr(svr,index,str,path,solopt):
  """
rtksvropenstr(rtksvr_t *svr, int index, int str, const char *path,
                          const solopt_t *solopt)"""

  if(type(svr) == rtksvr_t):
    svr = ctypes.byref(svr)

  if(type(solopt) == solopt_t):
    solopt = ctypes.byref(solopt)

  result = rtklib.rtksvropenstr(svr,index,str,path,solopt)


  return result

rtklib.rtksvrclosestr.argtypes = [ctypes.POINTER(rtksvr_t),ctypes.c_int]
rtklib.rtksvrclosestr.restype = None
def rtksvrclosestr(svr,index):
  """
rtksvrclosestr(rtksvr_t *svr, int index)"""

  if(type(svr) == rtksvr_t):
    svr = ctypes.byref(svr)

  result = rtklib.rtksvrclosestr(svr,index)


  return result

rtklib.rtksvrlock.argtypes = [ctypes.POINTER(rtksvr_t)]
rtklib.rtksvrlock.restype = None
def rtksvrlock(svr):
  """
rtksvrlock  (rtksvr_t *svr)"""

  if(type(svr) == rtksvr_t):
    svr = ctypes.byref(svr)

  result = rtklib.rtksvrlock(svr)


  return result

rtklib.rtksvrunlock.argtypes = [ctypes.POINTER(rtksvr_t)]
rtklib.rtksvrunlock.restype = None
def rtksvrunlock(svr):
  """
rtksvrunlock(rtksvr_t *svr)"""

  if(type(svr) == rtksvr_t):
    svr = ctypes.byref(svr)

  result = rtklib.rtksvrunlock(svr)


  return result

rtklib.rtksvrostat.argtypes = [ctypes.POINTER(rtksvr_t),ctypes.c_int,ctypes.POINTER(gtime_t),ctypes.POINTER(ctypes.c_int),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_void_p),ctypes.POINTER(ctypes.c_int)]
rtklib.rtksvrostat.restype = ctypes.c_int
def rtksvrostat(svr,type,time,sat,az,el,snr,vsat):
  """
rtksvrostat (rtksvr_t *svr, int type, gtime_t *time, int *sat,
                         double *az, double *el, int **snr, int *vsat)"""

  if(type(svr) == rtksvr_t):
    svr = ctypes.byref(svr)

  if(type(time) == gtime_t):
    time = ctypes.byref(time)

  result = rtklib.rtksvrostat(svr,type,time,sat,az,el,snr,vsat)


  return result

rtklib.rtksvrsstat.argtypes = [ctypes.POINTER(rtksvr_t),ctypes.POINTER(ctypes.c_int),ctypes.POINTER(ctypes.c_char)]
rtklib.rtksvrsstat.restype = None
def rtksvrsstat(svr,sstat,msg):
  """
rtksvrsstat (rtksvr_t *svr, int *sstat, char *msg)"""

  if(type(svr) == rtksvr_t):
    svr = ctypes.byref(svr)

  result = rtklib.rtksvrsstat(svr,sstat,msg)


  return result

rtklib.dl_readurls.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.POINTER(ctypes.c_void_p),ctypes.c_int,ctypes.POINTER(url_t),ctypes.c_int]
rtklib.dl_readurls.restype = ctypes.c_int
def dl_readurls(file,types,ntype,urls,nmax):
  """
dl_readurls(const char *file, char **types, int ntype, url_t *urls,
                       int nmax)"""

  if(type(urls) == url_t):
    urls = ctypes.byref(urls)

  result = rtklib.dl_readurls(file,types,ntype,urls,nmax)


  return result

rtklib.dl_readstas.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.POINTER(ctypes.c_void_p),ctypes.c_int]
rtklib.dl_readstas.restype = ctypes.c_int
def dl_readstas(file,stas,nmax):
  """
dl_readstas(const char *file, char **stas, int nmax)"""

  result = rtklib.dl_readstas(file,stas,nmax)


  return result

rtklib.dl_exec.argtypes = [gtime_t,gtime_t,ctypes.c_double,ctypes.c_int,ctypes.c_int,ctypes.POINTER(url_t),ctypes.c_int,ctypes.POINTER(ctypes.c_void_p),ctypes.c_int,ctypes.POINTER(ctypes.c_char),ctypes.POINTER(ctypes.c_char),ctypes.POINTER(ctypes.c_char),ctypes.POINTER(ctypes.c_char),ctypes.c_int,ctypes.POINTER(ctypes.c_char),ctypes.POINTER(None)]
rtklib.dl_exec.restype = ctypes.c_int
def dl_exec(ts,te,ti,seqnos,seqnoe,urls,nurl,stas,nsta,dir,usr,pwd,proxy,opts,msg,fp):
  """
dl_exec(gtime_t ts, gtime_t te, double ti, int seqnos, int seqnoe,
                   const url_t *urls, int nurl, char **stas, int nsta,
                   const char *dir, const char *usr, const char *pwd,
                   const char *proxy, int opts, char *msg, FILE *fp)"""

  if(type(urls) == url_t):
    urls = ctypes.byref(urls)

  result = rtklib.dl_exec(ts,te,ti,seqnos,seqnoe,urls,nurl,stas,nsta,dir,usr,pwd,proxy,opts,msg,fp)


  return result

rtklib.dl_test.argtypes = [gtime_t,gtime_t,ctypes.c_double,ctypes.POINTER(url_t),ctypes.c_int,ctypes.POINTER(ctypes.c_void_p),ctypes.c_int,ctypes.POINTER(ctypes.c_char),ctypes.c_int,ctypes.c_int,ctypes.POINTER(None)]
rtklib.dl_test.restype = None
def dl_test(ts,te,ti,urls,nurl,stas,nsta,dir,ncol,datefmt,fp):
  """
dl_test(gtime_t ts, gtime_t te, double ti, const url_t *urls,
                    int nurl, char **stas, int nsta, const char *dir,
                    int ncol, int datefmt, FILE *fp)"""

  if(type(urls) == url_t):
    urls = ctypes.byref(urls)

  result = rtklib.dl_test(ts,te,ti,urls,nurl,stas,nsta,dir,ncol,datefmt,fp)


  return result

rtklib.showmsg.argtypes = [ctypes.POINTER(ctypes.c_char)]
rtklib.showmsg.restype = ctypes.c_int
def showmsg(format):
  """
showmsg(char *format,...)"""

  result = rtklib.showmsg(format)


  return result

rtklib.settspan.argtypes = [gtime_t,gtime_t]
rtklib.settspan.restype = None
def settspan(ts,te):
  """
settspan(gtime_t ts, gtime_t te)"""

  result = rtklib.settspan(ts,te)


  return result

rtklib.settime.argtypes = [gtime_t]
rtklib.settime.restype = None
def settime(time):
  """
settime(gtime_t time)"""

  result = rtklib.settime(time)


  return result

rtklib.lexupdatecorr.argtypes = [ctypes.POINTER(lexmsg_t),ctypes.POINTER(nav_t),ctypes.POINTER(gtime_t)]
rtklib.lexupdatecorr.restype = ctypes.c_int
def lexupdatecorr(msg,nav,tof):
  """
lexupdatecorr(const lexmsg_t *msg, nav_t *nav, gtime_t *tof)"""

  if(type(msg) == lexmsg_t):
    msg = ctypes.byref(msg)

  if(type(nav) == nav_t):
    nav = ctypes.byref(nav)

  if(type(tof) == gtime_t):
    tof = ctypes.byref(tof)

  result = rtklib.lexupdatecorr(msg,nav,tof)


  return result

rtklib.lexreadmsg.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.c_int,ctypes.POINTER(lex_t)]
rtklib.lexreadmsg.restype = ctypes.c_int
def lexreadmsg(file,sel,lex):
  """
lexreadmsg(const char *file, int sel, lex_t *lex)"""

  if(type(lex) == lex_t):
    lex = ctypes.byref(lex)

  result = rtklib.lexreadmsg(file,sel,lex)


  return result

rtklib.lexoutmsg.argtypes = [ctypes.POINTER(None),ctypes.POINTER(lexmsg_t)]
rtklib.lexoutmsg.restype = None
def lexoutmsg(fp,msg):
  """
lexoutmsg(FILE *fp, const lexmsg_t *msg)"""

  if(type(msg) == lexmsg_t):
    msg = ctypes.byref(msg)

  result = rtklib.lexoutmsg(fp,msg)


  return result

rtklib.lexconvbin.argtypes = [ctypes.c_int,ctypes.c_int,ctypes.POINTER(ctypes.c_char),ctypes.POINTER(ctypes.c_char)]
rtklib.lexconvbin.restype = ctypes.c_int
def lexconvbin(type,format,infile,outfile):
  """
lexconvbin(int type, int format, const char *infile,
                      const char *outfile)"""

  result = rtklib.lexconvbin(type,format,infile,outfile)


  return result

rtklib.lexeph2pos.argtypes = [gtime_t,ctypes.c_int,ctypes.POINTER(nav_t),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
rtklib.lexeph2pos.restype = ctypes.c_int
def lexeph2pos(time,sat,nav,rs,dts,var):
  """
lexeph2pos(gtime_t time, int sat, const nav_t *nav, double *rs,
                      double *dts, double *var)"""

  if(type(nav) == nav_t):
    nav = ctypes.byref(nav)

  result = rtklib.lexeph2pos(time,sat,nav,rs,dts,var)


  return result

rtklib.lexioncorr.argtypes = [gtime_t,ctypes.POINTER(nav_t),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
rtklib.lexioncorr.restype = ctypes.c_int
def lexioncorr(time,nav,pos,azel,delay,var):
  """
lexioncorr(gtime_t time, const nav_t *nav, const double *pos,
                      const double *azel, double *delay, double *var)"""

  if(type(nav) == nav_t):
    nav = ctypes.byref(nav)

  result = rtklib.lexioncorr(time,nav,pos,azel,delay,var)


  return result


