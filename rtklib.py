
import ctypes
import warnings
#run `pip install enum34` if your getting a failure on the next line
import enum

if not hasattr(ctypes,'c_int128'):
    ctypes.c_int128 = ctypes.c_int64*2
    ctypes.c_uint128 = ctypes.c_uint64*2
my_endian=ctypes.Structure

lib_file = "librtk"
import os
import sys

ext = {'darwin':'dylib','linux':'so','linux2':'so','win32':'dll'}
lib_file += '.' + ext[sys.platform]

path = os.path.dirname(__file__)
lib_file = os.path.join(path, lib_file)

librtk = ctypes.CDLL(lib_file)

class CODES(enum.Enum):
    CODE_NONE = 0
    L1C       = 1
    L1P       = 2
    L1W       = 3
    L1Y       = 4
    L1M       = 5
    L1N       = 6
    L1S       = 7
    L1L       = 8
    L1E       = 9
    L1A       = 10
    L1B       = 11
    L1X       = 12
    L1Z       = 13
    L2C       = 14
    L2D       = 15
    L2S       = 16
    L2L       = 17
    L2X       = 18
    L2P       = 19
    L2W       = 20
    L2Y       = 21
    L2M       = 22
    L2N       = 23
    L5I       = 24
    L5Q       = 25
    L5X       = 26
    L7I       = 27
    L7Q       = 28
    L7X       = 29
    L6A       = 30
    L6B       = 31
    L6C       = 32
    L6X       = 33
    L6Z       = 34
    L6S       = 35
    L6L       = 36
    L8I       = 37
    L8Q       = 38
    L8X       = 39
    L2I       = 40
    L2Q       = 41
    L6I       = 42
    L6Q       = 43
    L3I       = 44
    L3Q       = 45
    L3X       = 46
    L1I       = 47
    L1Q       = 48
    L5A       = 49
    L5B       = 50
    L5C       = 51
    L9A       = 52
    L9B       = 53
    L9C       = 54
    L9X       = 55
    L1D       = 56
    L5D       = 57
    L5P       = 58
    L5Z       = 59
    L6E       = 60
    L7D       = 61
    L7P       = 62
    L7Z       = 63
    L8D       = 64
    L8P       = 65
    L4A       = 66
    L4B       = 67
    L4X       = 68





class gtime_t (my_endian):
    """
struct {        /* time struct */
    time_t time;        /* time (s) expressed by standard time_t */
    double sec;         /* fraction of second under 1 s */
"""
    _pack_ = 1
    _fields_ = [ ("time" , ctypes.c_int64  ),
                 ("sec"  , ctypes.c_double )]
    def SetConstants(self):
        """ Sets Constant fields to their default values """ 
        pass


class obsd_t (my_endian):
    """
struct {        /* observation data record */
    gtime_t time;       /* receiver sampling time (GPST) */
    uint8_t sat,rcv;    /* satellite/receiver number */
    uint16_t SNR[NFREQ+NEXOBS]; /* signal strength (0.001 dBHz) */
    uint8_t  LLI[NFREQ+NEXOBS]; /* loss of lock indicator */
    uint8_t code[NFREQ+NEXOBS]; /* code indicator (CODE_???) */
    double L[NFREQ+NEXOBS]; /* observation data carrier-phase (cycle) */
    double P[NFREQ+NEXOBS]; /* observation data pseudorange (m) */
    float  D[NFREQ+NEXOBS]; /* observation data doppler frequency (Hz) */
"""
    _pack_ = 1
    _fields_ = [ ("time"             , gtime_t             ),
                 ("sat"              , ctypes.c_ubyte      ),
                 ("rcv"              , ctypes.c_ubyte      ),
                 ("SNR"              , ctypes.c_uint16 * 3 ),
                 ("LLI"              , ctypes.c_ubyte  * 3 ),
                 ("code"             , ctypes.c_ubyte  * 3 ),
                 ("Padding_240_256_" , ctypes.c_ubyte  * 2 ),
                 ("L"                , ctypes.c_double * 3 ),
                 ("P"                , ctypes.c_double * 3 ),
                 ("D"                , ctypes.c_float  * 3 ),
                 ("Padding_736_"     , ctypes.c_ubyte  * 4 )]
    def SetConstants(self):
        """ Sets Constant fields to their default values """ 
        pass


class obs_t (my_endian):
    """
struct {        /* observation data */
    int n,nmax;         /* number of obervation data/allocated */
    obsd_t *data;       /* observation data records */
"""
    _pack_ = 1
    _fields_ = [ ("n"    , ctypes.c_int32        ),
                 ("nmax" , ctypes.c_int32        ),
                 ("data" , ctypes.POINTER(obsd_t ) )]
    def SetConstants(self):
        """ Sets Constant fields to their default values """ 
        pass


class erpd_t (my_endian):
    """
struct {        /* earth rotation parameter data type */
    double mjd;         /* mjd (days) */
    double xp,yp;       /* pole offset (rad) */
    double xpr,ypr;     /* pole offset rate (rad/day) */
    double ut1_utc;     /* ut1-utc (s) */
    double lod;         /* length of day (s/day) */
"""
    _pack_ = 1
    _fields_ = [ ("mjd"     , ctypes.c_double ),
                 ("xp"      , ctypes.c_double ),
                 ("yp"      , ctypes.c_double ),
                 ("xpr"     , ctypes.c_double ),
                 ("ypr"     , ctypes.c_double ),
                 ("ut1_utc" , ctypes.c_double ),
                 ("lod"     , ctypes.c_double )]
    def SetConstants(self):
        """ Sets Constant fields to their default values """ 
        pass


class erp_t (my_endian):
    """
struct {        /* earth rotation parameter type */
    int n,nmax;         /* number and max number of data */
    erpd_t *data;       /* earth rotation parameter data */
"""
    _pack_ = 1
    _fields_ = [ ("n"    , ctypes.c_int32        ),
                 ("nmax" , ctypes.c_int32        ),
                 ("data" , ctypes.POINTER(erpd_t ) )]
    def SetConstants(self):
        """ Sets Constant fields to their default values """ 
        pass


class pcv_t (my_endian):
    """
struct {        /* antenna parameter type */
    int sat;            /* satellite number (0:receiver) */
    char type[MAXANT];  /* antenna type */
    char code[MAXANT];  /* serial number or satellite code */
    gtime_t ts,te;      /* valid time start and end */
    double off[NFREQ][ 3]; /* phase center offset e/n/u or x/y/z (m) */
    double var[NFREQ][19]; /* phase center variation (m) */
                        /* el=90,85,...,0 or nadir=0,1,2,3,... (deg) */
"""
    _pack_ = 1
    _fields_ = [ ("sat"                , ctypes.c_int32        ),
                 ("type"               , ctypes.c_char    * 64 ),
                 ("code"               , ctypes.c_char    * 64 ),
                 ("Padding_1056_1088_" , ctypes.c_ubyte   * 4  ),
                 ("ts"                 , gtime_t               ),
                 ("te"                 , gtime_t               ),
                 ("off"                , (ctypes.c_double * 3  ) * 3 ),
                 ("var"                , (ctypes.c_double * 19 ) * 3 )]
    def SetConstants(self):
        """ Sets Constant fields to their default values """ 
        pass


class pcvs_t (my_endian):
    """
struct {        /* antenna parameters type */
    int n,nmax;         /* number of data/allocated */
    pcv_t *pcv;         /* antenna parameters data */
"""
    _pack_ = 1
    _fields_ = [ ("n"    , ctypes.c_int32       ),
                 ("nmax" , ctypes.c_int32       ),
                 ("pcv"  , ctypes.POINTER(pcv_t ) )]
    def SetConstants(self):
        """ Sets Constant fields to their default values """ 
        pass


class alm_t (my_endian):
    """
struct {        /* almanac type */
    int sat;            /* satellite number */
    int svh;            /* sv health (0:ok) */
    int svconf;         /* as and sv config */
    int week;           /* GPS/QZS: gps week, GAL: galileo week */
    gtime_t toa;        /* Toa */
                        /* SV orbit parameters */
    double A,e,i0,OMG0,omg,M0,OMGd;
    double toas;        /* Toa (s) in week */
    double f0,f1;       /* SV clock parameters (af0,af1) */
"""
    _pack_ = 1
    _fields_ = [ ("sat"    , ctypes.c_int32  ),
                 ("svh"    , ctypes.c_int32  ),
                 ("svconf" , ctypes.c_int32  ),
                 ("week"   , ctypes.c_int32  ),
                 ("toa"    , gtime_t         ),
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
        """ Sets Constant fields to their default values """ 
        pass


class eph_t (my_endian):
    """
struct {        /* GPS/QZS/GAL broadcast ephemeris type */
    int sat;            /* satellite number */
    int iode,iodc;      /* IODE,IODC */
    int sva;            /* SV accuracy (URA index) */
    int svh;            /* SV health (0:ok) */
    int week;           /* GPS/QZS: gps week, GAL: galileo week */
    int code;           /* GPS/QZS: code on L2 */
                        /* GAL: data source defined as rinex 3.03 */
                        /* BDS: data source (0:unknown,1:B1I,2:B1Q,3:B2I,4:B2Q,5:B3I,6:B3Q) */
    int flag;           /* GPS/QZS: L2 P data flag */
                        /* BDS: nav type (0:unknown,1:IGSO/MEO,2:GEO) */
    gtime_t toe,toc,ttr; /* Toe,Toc,T_trans */
                        /* SV orbit parameters */
    double A,e,i0,OMG0,omg,M0,deln,OMGd,idot;
    double crc,crs,cuc,cus,cic,cis;
    double toes;        /* Toe (s) in week */
    double fit;         /* fit interval (h) */
    double f0,f1,f2;    /* SV clock parameters (af0,af1,af2) */
    double tgd[6];      /* group delay parameters */
                        /* GPS/QZS:tgd[0]=TGD */
                        /* GAL:tgd[0]=BGD_E1E5a,tgd[1]=BGD_E1E5b */
                        /* CMP:tgd[0]=TGD_B1I ,tgd[1]=TGD_B2I/B2b,tgd[2]=TGD_B1Cp */
                        /*     tgd[3]=TGD_B2ap,tgd[4]=ISC_B1Cd   ,tgd[5]=ISC_B2ad */
    double Adot,ndot;   /* Adot,ndot for CNAV */
"""
    _pack_ = 1
    _fields_ = [ ("sat"  , ctypes.c_int32      ),
                 ("iode" , ctypes.c_int32      ),
                 ("iodc" , ctypes.c_int32      ),
                 ("sva"  , ctypes.c_int32      ),
                 ("svh"  , ctypes.c_int32      ),
                 ("week" , ctypes.c_int32      ),
                 ("code" , ctypes.c_int32      ),
                 ("flag" , ctypes.c_int32      ),
                 ("toe"  , gtime_t             ),
                 ("toc"  , gtime_t             ),
                 ("ttr"  , gtime_t             ),
                 ("A"    , ctypes.c_double     ),
                 ("e"    , ctypes.c_double     ),
                 ("i0"   , ctypes.c_double     ),
                 ("OMG0" , ctypes.c_double     ),
                 ("omg"  , ctypes.c_double     ),
                 ("M0"   , ctypes.c_double     ),
                 ("deln" , ctypes.c_double     ),
                 ("OMGd" , ctypes.c_double     ),
                 ("idot" , ctypes.c_double     ),
                 ("crc"  , ctypes.c_double     ),
                 ("crs"  , ctypes.c_double     ),
                 ("cuc"  , ctypes.c_double     ),
                 ("cus"  , ctypes.c_double     ),
                 ("cic"  , ctypes.c_double     ),
                 ("cis"  , ctypes.c_double     ),
                 ("toes" , ctypes.c_double     ),
                 ("fit"  , ctypes.c_double     ),
                 ("f0"   , ctypes.c_double     ),
                 ("f1"   , ctypes.c_double     ),
                 ("f2"   , ctypes.c_double     ),
                 ("tgd"  , ctypes.c_double * 6 ),
                 ("Adot" , ctypes.c_double     ),
                 ("ndot" , ctypes.c_double     )]
    def SetConstants(self):
        """ Sets Constant fields to their default values """ 
        pass


class geph_t (my_endian):
    """
struct {        /* GLONASS broadcast ephemeris type */
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
"""
    _pack_ = 1
    _fields_ = [ ("sat"   , ctypes.c_int32      ),
                 ("iode"  , ctypes.c_int32      ),
                 ("frq"   , ctypes.c_int32      ),
                 ("svh"   , ctypes.c_int32      ),
                 ("sva"   , ctypes.c_int32      ),
                 ("age"   , ctypes.c_int32      ),
                 ("toe"   , gtime_t             ),
                 ("tof"   , gtime_t             ),
                 ("pos"   , ctypes.c_double * 3 ),
                 ("vel"   , ctypes.c_double * 3 ),
                 ("acc"   , ctypes.c_double * 3 ),
                 ("taun"  , ctypes.c_double     ),
                 ("gamn"  , ctypes.c_double     ),
                 ("dtaun" , ctypes.c_double     )]
    def SetConstants(self):
        """ Sets Constant fields to their default values """ 
        pass


class peph_t (my_endian):
    """
struct {        /* precise ephemeris type */
    gtime_t time;       /* time (GPST) */
    int index;          /* ephemeris index for multiple files */
    double pos[MAXSAT][4]; /* satellite position/clock (ecef) (m|s) */
    float  std[MAXSAT][4]; /* satellite position/clock std (m|s) */
    double vel[MAXSAT][4]; /* satellite velocity/clk-rate (m/s|s/s) */
    float  vst[MAXSAT][4]; /* satellite velocity/clk-rate std (m/s|s/s) */
    float  cov[MAXSAT][3]; /* satellite position covariance (m^2) */
    float  vco[MAXSAT][3]; /* satellite velocity covariance (m^2) */
"""
    _pack_ = 1
    _fields_ = [ ("time"             , gtime_t              ),
                 ("index"            , ctypes.c_int32       ),
                 ("Padding_160_192_" , ctypes.c_ubyte   * 4 ),
                 ("pos"              , (ctypes.c_double * 4 ) * 71 ),
                 ("std"              , (ctypes.c_float  * 4 ) * 71 ),
                 ("vel"              , (ctypes.c_double * 4 ) * 71 ),
                 ("vst"              , (ctypes.c_float  * 4 ) * 71 ),
                 ("cov"              , (ctypes.c_float  * 3 ) * 71 ),
                 ("vco"              , (ctypes.c_float  * 3 ) * 71 )]
    def SetConstants(self):
        """ Sets Constant fields to their default values """ 
        pass


class pclk_t (my_endian):
    """
struct {        /* precise clock type */
    gtime_t time;       /* time (GPST) */
    int index;          /* clock index for multiple files */
    double clk[MAXSAT][1]; /* satellite clock (s) */
    float  std[MAXSAT][1]; /* satellite clock std (s) */
"""
    _pack_ = 1
    _fields_ = [ ("time"             , gtime_t              ),
                 ("index"            , ctypes.c_int32       ),
                 ("Padding_160_192_" , ctypes.c_ubyte   * 4 ),
                 ("clk"              , (ctypes.c_double * 1 ) * 71 ),
                 ("std"              , (ctypes.c_float  * 1 ) * 71 ),
                 ("Padding_7008_"    , ctypes.c_ubyte   * 4 )]
    def SetConstants(self):
        """ Sets Constant fields to their default values """ 
        pass


class seph_t (my_endian):
    """
struct {        /* SBAS ephemeris type */
    int sat;            /* satellite number */
    gtime_t t0;         /* reference epoch time (GPST) */
    gtime_t tof;        /* time of message frame (GPST) */
    int sva;            /* SV accuracy (URA index) */
    int svh;            /* SV health (0:ok) */
    double pos[3];      /* satellite position (m) (ecef) */
    double vel[3];      /* satellite velocity (m/s) (ecef) */
    double acc[3];      /* satellite acceleration (m/s^2) (ecef) */
    double af0,af1;     /* satellite clock-offset/drift (s,s/s) */
"""
    _pack_ = 1
    _fields_ = [ ("sat"            , ctypes.c_int32      ),
                 ("Padding_32_64_" , ctypes.c_ubyte  * 4 ),
                 ("t0"             , gtime_t             ),
                 ("tof"            , gtime_t             ),
                 ("sva"            , ctypes.c_int32      ),
                 ("svh"            , ctypes.c_int32      ),
                 ("pos"            , ctypes.c_double * 3 ),
                 ("vel"            , ctypes.c_double * 3 ),
                 ("acc"            , ctypes.c_double * 3 ),
                 ("af0"            , ctypes.c_double     ),
                 ("af1"            , ctypes.c_double     )]
    def SetConstants(self):
        """ Sets Constant fields to their default values """ 
        pass


class tled_t (my_endian):
    """
struct {        /* NORAL TLE data type */
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
"""
    _pack_ = 1
    _fields_ = [ ("name"             , ctypes.c_char  * 32 ),
                 ("alias"            , ctypes.c_char  * 32 ),
                 ("satno"            , ctypes.c_char  * 16 ),
                 ("satclass"         , ctypes.c_char       ),
                 ("desig"            , ctypes.c_char  * 16 ),
                 ("Padding_776_832_" , ctypes.c_ubyte * 7  ),
                 ("epoch"            , gtime_t             ),
                 ("ndot"             , ctypes.c_double     ),
                 ("nddot"            , ctypes.c_double     ),
                 ("bstar"            , ctypes.c_double     ),
                 ("etype"            , ctypes.c_int32      ),
                 ("eleno"            , ctypes.c_int32      ),
                 ("inc"              , ctypes.c_double     ),
                 ("OMG"              , ctypes.c_double     ),
                 ("ecc"              , ctypes.c_double     ),
                 ("omg"              , ctypes.c_double     ),
                 ("M"                , ctypes.c_double     ),
                 ("n"                , ctypes.c_double     ),
                 ("rev"              , ctypes.c_int32      ),
                 ("Padding_1632_"    , ctypes.c_ubyte * 4  )]
    def SetConstants(self):
        """ Sets Constant fields to their default values """ 
        pass


class tle_t (my_endian):
    """
struct {        /* NORAD TLE (two line element) type */
    int n,nmax;         /* number/max number of two line element data */
    tled_t *data;       /* NORAD TLE data */
"""
    _pack_ = 1
    _fields_ = [ ("n"    , ctypes.c_int32        ),
                 ("nmax" , ctypes.c_int32        ),
                 ("data" , ctypes.POINTER(tled_t ) )]
    def SetConstants(self):
        """ Sets Constant fields to their default values """ 
        pass


class tec_t (my_endian):
    """
struct {        /* TEC grid type */
    gtime_t time;       /* epoch time (GPST) */
    int ndata[3];       /* TEC grid data size {nlat,nlon,nhgt} */
    double rb;          /* earth radius (km) */
    double lats[3];     /* latitude start/interval (deg) */
    double lons[3];     /* longitude start/interval (deg) */
    double hgts[3];     /* heights start/interval (km) */
    double *data;       /* TEC grid data (tecu) */
    float *rms;         /* RMS values (tecu) */
"""
    _pack_ = 1
    _fields_ = [ ("time"             , gtime_t                        ),
                 ("ndata"            , ctypes.c_int32  * 3            ),
                 ("Padding_224_256_" , ctypes.c_ubyte  * 4            ),
                 ("rb"               , ctypes.c_double                ),
                 ("lats"             , ctypes.c_double * 3            ),
                 ("lons"             , ctypes.c_double * 3            ),
                 ("hgts"             , ctypes.c_double * 3            ),
                 ("data"             , ctypes.POINTER(ctypes.c_double ) ),
                 ("rms"              , ctypes.POINTER(ctypes.c_float  ) )]
    def SetConstants(self):
        """ Sets Constant fields to their default values """ 
        pass


class sbsmsg_t (my_endian):
    """
struct {        /* SBAS message type */
    int week,tow;       /* receiption time */
    uint8_t prn,rcv;    /* SBAS satellite PRN,receiver number */
    uint8_t msg[29];    /* SBAS message (226bit) padded by 0 */
"""
    _pack_ = 1
    _fields_ = [ ("week"         , ctypes.c_int32      ),
                 ("tow"          , ctypes.c_int32      ),
                 ("prn"          , ctypes.c_ubyte      ),
                 ("rcv"          , ctypes.c_ubyte      ),
                 ("msg"          , ctypes.c_ubyte * 29 ),
                 ("Padding_312_" , ctypes.c_ubyte * 1  )]
    def SetConstants(self):
        """ Sets Constant fields to their default values """ 
        pass


class sbs_t (my_endian):
    """
struct {        /* SBAS messages type */
    int n,nmax;         /* number of SBAS messages/allocated */
    sbsmsg_t *msgs;     /* SBAS messages */
"""
    _pack_ = 1
    _fields_ = [ ("n"    , ctypes.c_int32          ),
                 ("nmax" , ctypes.c_int32          ),
                 ("msgs" , ctypes.POINTER(sbsmsg_t ) )]
    def SetConstants(self):
        """ Sets Constant fields to their default values """ 
        pass


class sbsfcorr_t (my_endian):
    """
struct {        /* SBAS fast correction type */
    gtime_t t0;         /* time of applicability (TOF) */
    double prc;         /* pseudorange correction (PRC) (m) */
    double rrc;         /* range-rate correction (RRC) (m/s) */
    double dt;          /* range-rate correction delta-time (s) */
    int iodf;           /* IODF (issue of date fast corr) */
    int16_t udre;       /* UDRE+1 */
    int16_t ai;         /* degradation factor indicator */
"""
    _pack_ = 1
    _fields_ = [ ("t0"   , gtime_t         ),
                 ("prc"  , ctypes.c_double ),
                 ("rrc"  , ctypes.c_double ),
                 ("dt"   , ctypes.c_double ),
                 ("iodf" , ctypes.c_int32  ),
                 ("udre" , ctypes.c_int16  ),
                 ("ai"   , ctypes.c_int16  )]
    def SetConstants(self):
        """ Sets Constant fields to their default values """ 
        pass


class sbslcorr_t (my_endian):
    """
struct {        /* SBAS long term satellite error correction type */
    gtime_t t0;         /* correction time */
    int iode;           /* IODE (issue of date ephemeris) */
    double dpos[3];     /* delta position (m) (ecef) */
    double dvel[3];     /* delta velocity (m/s) (ecef) */
    double daf0,daf1;   /* delta clock-offset/drift (s,s/s) */
"""
    _pack_ = 1
    _fields_ = [ ("t0"               , gtime_t             ),
                 ("iode"             , ctypes.c_int32      ),
                 ("Padding_160_192_" , ctypes.c_ubyte  * 4 ),
                 ("dpos"             , ctypes.c_double * 3 ),
                 ("dvel"             , ctypes.c_double * 3 ),
                 ("daf0"             , ctypes.c_double     ),
                 ("daf1"             , ctypes.c_double     )]
    def SetConstants(self):
        """ Sets Constant fields to their default values """ 
        pass


class sbssatp_t (my_endian):
    """
struct {        /* SBAS satellite correction type */
    int sat;            /* satellite number */
    sbsfcorr_t fcorr;   /* fast correction */
    sbslcorr_t lcorr;   /* long term correction */
"""
    _pack_ = 1
    _fields_ = [ ("sat"            , ctypes.c_int32     ),
                 ("Padding_32_64_" , ctypes.c_ubyte * 4 ),
                 ("fcorr"          , sbsfcorr_t         ),
                 ("lcorr"          , sbslcorr_t         )]
    def SetConstants(self):
        """ Sets Constant fields to their default values """ 
        pass


class sbssat_t (my_endian):
    """
struct {        /* SBAS satellite corrections type */
    int iodp;           /* IODP (issue of date mask) */
    int nsat;           /* number of satellites */
    int tlat;           /* system latency (s) */
    sbssatp_t sat[MAXSAT]; /* satellite correction */
"""
    _pack_ = 1
    _fields_ = [ ("iodp"            , ctypes.c_int32      ),
                 ("nsat"            , ctypes.c_int32      ),
                 ("tlat"            , ctypes.c_int32      ),
                 ("Padding_96_128_" , ctypes.c_ubyte * 4  ),
                 ("sat"             , sbssatp_t      * 71 )]
    def SetConstants(self):
        """ Sets Constant fields to their default values """ 
        pass


class sbsigp_t (my_endian):
    """
struct {        /* SBAS ionospheric correction type */
    gtime_t t0;         /* correction time */
    int16_t lat,lon;    /* latitude/longitude (deg) */
    int16_t give;       /* GIVI+1 */
    float delay;        /* vertical delay estimate (m) */
"""
    _pack_ = 1
    _fields_ = [ ("t0"               , gtime_t            ),
                 ("lat"              , ctypes.c_int16     ),
                 ("lon"              , ctypes.c_int16     ),
                 ("give"             , ctypes.c_int16     ),
                 ("Padding_176_192_" , ctypes.c_ubyte * 2 ),
                 ("delay"            , ctypes.c_float     ),
                 ("Padding_224_"     , ctypes.c_ubyte * 4 )]
    def SetConstants(self):
        """ Sets Constant fields to their default values """ 
        pass


class sbsigpband_t (my_endian):
    """
struct {        /* IGP band type */
    int16_t x;          /* longitude/latitude (deg) */
    const int16_t *y;   /* latitudes/longitudes (deg) */
    uint8_t bits;       /* IGP mask start bit */
    uint8_t bite;       /* IGP mask end bit */
"""
    _pack_ = 1
    _fields_ = [ ("x"              , ctypes.c_int16                ),
                 ("Padding_16_64_" , ctypes.c_ubyte * 6            ),
                 ("y"              , ctypes.POINTER(ctypes.c_int16 ) ),
                 ("bits"           , ctypes.c_ubyte                ),
                 ("bite"           , ctypes.c_ubyte                ),
                 ("Padding_144_"   , ctypes.c_ubyte * 6            )]
    def SetConstants(self):
        """ Sets Constant fields to their default values """ 
        pass


class sbsion_t (my_endian):
    """
struct {        /* SBAS ionospheric corrections type */
    int iodi;           /* IODI (issue of date ionos corr) */
    int nigp;           /* number of igps */
    sbsigp_t igp[MAXNIGP]; /* ionospheric correction */
"""
    _pack_ = 1
    _fields_ = [ ("iodi" , ctypes.c_int32 ),
                 ("nigp" , ctypes.c_int32 ),
                 ("igp"  , sbsigp_t * 201 )]
    def SetConstants(self):
        """ Sets Constant fields to their default values """ 
        pass


class dgps_t (my_endian):
    """
struct {        /* DGPS/GNSS correction type */
    gtime_t t0;         /* correction time */
    double prc;         /* pseudorange correction (PRC) (m) */
    double rrc;         /* range rate correction (RRC) (m/s) */
    int iod;            /* issue of data (IOD) */
    double udre;        /* UDRE */
"""
    _pack_ = 1
    _fields_ = [ ("t0"               , gtime_t            ),
                 ("prc"              , ctypes.c_double    ),
                 ("rrc"              , ctypes.c_double    ),
                 ("iod"              , ctypes.c_int32     ),
                 ("Padding_288_320_" , ctypes.c_ubyte * 4 ),
                 ("udre"             , ctypes.c_double    )]
    def SetConstants(self):
        """ Sets Constant fields to their default values """ 
        pass


class ssr_t (my_endian):
    """
struct {        /* SSR correction type */
    gtime_t t0[6];      /* epoch time (GPST) {eph,clk,hrclk,ura,bias,pbias} */
    double udi[6];      /* SSR update interval (s) */
    int iod[6];         /* iod ssr {eph,clk,hrclk,ura,bias,pbias} */
    int iode;           /* issue of data */
    int iodcrc;         /* issue of data crc for beidou/sbas */
    int ura;            /* URA indicator */
    int refd;           /* sat ref datum (0:ITRF,1:regional) */
    double deph [3];    /* delta orbit {radial,along,cross} (m) */
    double ddeph[3];    /* dot delta orbit {radial,along,cross} (m/s) */
    double dclk [3];    /* delta clock {c0,c1,c2} (m,m/s,m/s^2) */
    double hrclk;       /* high-rate clock corection (m) */
    float  cbias[MAXCODE]; /* code biases (m) */
    double pbias[MAXCODE]; /* phase biases (m) */
    float  stdpb[MAXCODE]; /* std-dev of phase biases (m) */
    double yaw_ang,yaw_rate; /* yaw angle and yaw rate (deg,deg/s) */
    uint8_t update;     /* update flag (0:no update,1:update) */
"""
    _pack_ = 1
    _fields_ = [ ("t0"             , gtime_t         * 6  ),
                 ("udi"            , ctypes.c_double * 6  ),
                 ("iod"            , ctypes.c_int32  * 6  ),
                 ("iode"           , ctypes.c_int32       ),
                 ("iodcrc"         , ctypes.c_int32       ),
                 ("ura"            , ctypes.c_int32       ),
                 ("refd"           , ctypes.c_int32       ),
                 ("deph"           , ctypes.c_double * 3  ),
                 ("ddeph"          , ctypes.c_double * 3  ),
                 ("dclk"           , ctypes.c_double * 3  ),
                 ("hrclk"          , ctypes.c_double      ),
                 ("cbias"          , ctypes.c_float  * 68 ),
                 ("pbias"          , ctypes.c_double * 68 ),
                 ("stdpb"          , ctypes.c_float  * 68 ),
                 ("yaw_ang"        , ctypes.c_double      ),
                 ("yaw_rate"       , ctypes.c_double      ),
                 ("update"         , ctypes.c_ubyte       ),
                 ("Padding_10952_" , ctypes.c_ubyte  * 7  )]
    def SetConstants(self):
        """ Sets Constant fields to their default values """ 
        pass


class nav_t (my_endian):
    """
struct {        /* navigation data type */
    int n,nmax;         /* number of broadcast ephemeris */
    int ng,ngmax;       /* number of glonass ephemeris */
    int ns,nsmax;       /* number of sbas ephemeris */
    int ne,nemax;       /* number of precise ephemeris */
    int nc,ncmax;       /* number of precise clock */
    int na,namax;       /* number of almanac data */
    int nt,ntmax;       /* number of tec grid data */
    eph_t *eph;         /* GPS/QZS/GAL/BDS/IRN ephemeris */
    geph_t *geph;       /* GLONASS ephemeris */
    seph_t *seph;       /* SBAS ephemeris */
    peph_t *peph;       /* precise ephemeris */
    pclk_t *pclk;       /* precise clock */
    alm_t *alm;         /* almanac data */
    tec_t *tec;         /* tec grid data */
    erp_t  erp;         /* earth rotation parameters */
    double utc_gps[8];  /* GPS delta-UTC parameters {A0,A1,Tot,WNt,dt_LS,WN_LSF,DN,dt_LSF} */
    double utc_glo[8];  /* GLONASS UTC time parameters {tau_C,tau_GPS} */
    double utc_gal[8];  /* Galileo UTC parameters */
    double utc_qzs[8];  /* QZS UTC parameters */
    double utc_cmp[8];  /* BeiDou UTC parameters */
    double utc_irn[9];  /* IRNSS UTC parameters {A0,A1,Tot,...,dt_LSF,A2} */
    double utc_sbs[4];  /* SBAS UTC parameters */
    double ion_gps[8];  /* GPS iono model parameters {a0,a1,a2,a3,b0,b1,b2,b3} */
    double ion_gal[4];  /* Galileo iono model parameters {ai0,ai1,ai2,0} */
    double ion_qzs[8];  /* QZSS iono model parameters {a0,a1,a2,a3,b0,b1,b2,b3} */
    double ion_cmp[8];  /* BeiDou iono model parameters {a0,a1,a2,a3,b0,b1,b2,b3} */
    double ion_irn[8];  /* IRNSS iono model parameters {a0,a1,a2,a3,b0,b1,b2,b3} */
    int glo_fcn[32];    /* GLONASS FCN + 8 */
    double cbias[MAXSAT][3]; /* satellite DCB (0:P1-P2,1:P1-C1,2:P2-C2) (m) */
    double rbias[MAXRCV][2][3]; /* receiver DCB (0:P1-P2,1:P1-C1,2:P2-C2) (m) */
    pcv_t pcvs[MAXSAT]; /* satellite antenna pcv */
    sbssat_t sbssat;    /* SBAS satellite corrections */
    sbsion_t sbsion[MAXBAND+1]; /* SBAS ionosphere corrections */
    dgps_t dgps[MAXSAT]; /* DGPS corrections */
    ssr_t ssr[MAXSAT];  /* SSR corrections */
"""
    _pack_ = 1
    _fields_ = [ ("n"       , ctypes.c_int32         ),
                 ("nmax"    , ctypes.c_int32         ),
                 ("ng"      , ctypes.c_int32         ),
                 ("ngmax"   , ctypes.c_int32         ),
                 ("ns"      , ctypes.c_int32         ),
                 ("nsmax"   , ctypes.c_int32         ),
                 ("ne"      , ctypes.c_int32         ),
                 ("nemax"   , ctypes.c_int32         ),
                 ("nc"      , ctypes.c_int32         ),
                 ("ncmax"   , ctypes.c_int32         ),
                 ("na"      , ctypes.c_int32         ),
                 ("namax"   , ctypes.c_int32         ),
                 ("nt"      , ctypes.c_int32         ),
                 ("ntmax"   , ctypes.c_int32         ),
                 ("eph"     , ctypes.POINTER(eph_t   ) ),
                 ("geph"    , ctypes.POINTER(geph_t  ) ),
                 ("seph"    , ctypes.POINTER(seph_t  ) ),
                 ("peph"    , ctypes.POINTER(peph_t  ) ),
                 ("pclk"    , ctypes.POINTER(pclk_t  ) ),
                 ("alm"     , ctypes.POINTER(alm_t   ) ),
                 ("tec"     , ctypes.POINTER(tec_t   ) ),
                 ("erp"     , erp_t                  ),
                 ("utc_gps" , ctypes.c_double   * 8  ),
                 ("utc_glo" , ctypes.c_double   * 8  ),
                 ("utc_gal" , ctypes.c_double   * 8  ),
                 ("utc_qzs" , ctypes.c_double   * 8  ),
                 ("utc_cmp" , ctypes.c_double   * 8  ),
                 ("utc_irn" , ctypes.c_double   * 9  ),
                 ("utc_sbs" , ctypes.c_double   * 4  ),
                 ("ion_gps" , ctypes.c_double   * 8  ),
                 ("ion_gal" , ctypes.c_double   * 4  ),
                 ("ion_qzs" , ctypes.c_double   * 8  ),
                 ("ion_cmp" , ctypes.c_double   * 8  ),
                 ("ion_irn" , ctypes.c_double   * 8  ),
                 ("glo_fcn" , ctypes.c_int32    * 32 ),
                 ("cbias"   , (ctypes.c_double  * 3  ) * 71 ),
                 ("rbias"   , ((ctypes.c_double * 3  ) * 2) * 64 ),
                 ("pcvs"    , pcv_t             * 71 ),
                 ("sbssat"  , sbssat_t               ),
                 ("sbsion"  , sbsion_t          * 11 ),
                 ("dgps"    , dgps_t            * 71 ),
                 ("ssr"     , ssr_t             * 71 )]
    def SetConstants(self):
        """ Sets Constant fields to their default values """ 
        pass


class sta_t (my_endian):
    """
struct {        /* station parameter type */
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
    int glo_cp_align;   /* GLONASS code-phase alignment (0:no,1:yes) */
    double glo_cp_bias[4]; /* GLONASS code-phase biases {1C,1P,2C,2P} (m) */
"""
    _pack_ = 1
    _fields_ = [ ("name"               , ctypes.c_char   * 64 ),
                 ("marker"             , ctypes.c_char   * 64 ),
                 ("antdes"             , ctypes.c_char   * 64 ),
                 ("antsno"             , ctypes.c_char   * 64 ),
                 ("rectype"            , ctypes.c_char   * 64 ),
                 ("recver"             , ctypes.c_char   * 64 ),
                 ("recsno"             , ctypes.c_char   * 64 ),
                 ("antsetup"           , ctypes.c_int32       ),
                 ("itrf"               , ctypes.c_int32       ),
                 ("deltype"            , ctypes.c_int32       ),
                 ("Padding_3680_3712_" , ctypes.c_ubyte  * 4  ),
                 ("pos"                , ctypes.c_double * 3  ),
                 ("del_"               , ctypes.c_double * 3  ),
                 ("hgt"                , ctypes.c_double      ),
                 ("glo_cp_align"       , ctypes.c_int32       ),
                 ("Padding_4192_4224_" , ctypes.c_ubyte  * 4  ),
                 ("glo_cp_bias"        , ctypes.c_double * 4  )]
    def SetConstants(self):
        """ Sets Constant fields to their default values """ 
        pass


class sol_t (my_endian):
    """
struct {        /* solution type */
    gtime_t time;       /* time (GPST) */
    double rr[6];       /* position/velocity (m|m/s) */
                        /* {x,y,z,vx,vy,vz} or {e,n,u,ve,vn,vu} */
    float  qr[6];       /* position variance/covariance (m^2) */
                        /* {c_xx,c_yy,c_zz,c_xy,c_yz,c_zx} or */
                        /* {c_ee,c_nn,c_uu,c_en,c_nu,c_ue} */
    float  qv[6];       /* velocity variance/covariance (m^2/s^2) */
    double dtr[6];      /* receiver clock bias to time systems (s) */
    uint8_t type;       /* type (0:xyz-ecef,1:enu-baseline) */
    uint8_t stat;       /* solution status (SOLQ_???) */
    uint8_t ns;         /* number of valid satellites */
    float age;          /* age of differential (s) */
    float ratio;        /* AR ratio factor for valiation */
    float thres;        /* AR ratio threshold for valiation */
"""
    _pack_ = 1
    _fields_ = [ ("time"               , gtime_t             ),
                 ("rr"                 , ctypes.c_double * 6 ),
                 ("qr"                 , ctypes.c_float  * 6 ),
                 ("qv"                 , ctypes.c_float  * 6 ),
                 ("dtr"                , ctypes.c_double * 6 ),
                 ("type"               , ctypes.c_ubyte      ),
                 ("stat"               , ctypes.c_ubyte      ),
                 ("ns"                 , ctypes.c_ubyte      ),
                 ("Padding_1304_1312_" , ctypes.c_ubyte  * 1 ),
                 ("age"                , ctypes.c_float      ),
                 ("ratio"              , ctypes.c_float      ),
                 ("thres"              , ctypes.c_float      )]
    def SetConstants(self):
        """ Sets Constant fields to their default values """ 
        pass


class solbuf_t (my_endian):
    """
struct {        /* solution buffer type */
    int n,nmax;         /* number of solution/max number of buffer */
    int cyclic;         /* cyclic buffer flag */
    int start,end;      /* start/end index */
    gtime_t time;       /* current solution time */
    sol_t *data;        /* solution data */
    double rb[3];       /* reference position {x,y,z} (ecef) (m) */
    uint8_t buff[MAXSOLMSG+1]; /* message buffer */
    int nb;             /* number of byte in message buffer */
"""
    _pack_ = 1
    _fields_ = [ ("n"                , ctypes.c_int32         ),
                 ("nmax"             , ctypes.c_int32         ),
                 ("cyclic"           , ctypes.c_int32         ),
                 ("start"            , ctypes.c_int32         ),
                 ("end"              , ctypes.c_int32         ),
                 ("Padding_160_192_" , ctypes.c_ubyte  * 4    ),
                 ("time"             , gtime_t                ),
                 ("data"             , ctypes.POINTER(sol_t   ) ),
                 ("rb"               , ctypes.c_double * 3    ),
                 ("buff"             , ctypes.c_ubyte  * 8192 ),
                 ("nb"               , ctypes.c_int32         ),
                 ("Padding_66144_"   , ctypes.c_ubyte  * 4    )]
    def SetConstants(self):
        """ Sets Constant fields to their default values """ 
        pass


class solstat_t (my_endian):
    """
struct {        /* solution status type */
    gtime_t time;       /* time (GPST) */
    uint8_t sat;        /* satellite number */
    uint8_t frq;        /* frequency (1:L1,2:L2,...) */
    float az,el;        /* azimuth/elevation angle (rad) */
    float resp;         /* pseudorange residual (m) */
    float resc;         /* carrier-phase residual (m) */
    uint8_t flag;       /* flags: (vsat<<5)+(slip<<3)+fix */
    uint16_t snr;       /* signal strength (*SNR_UNIT dBHz) */
    uint16_t lock;      /* lock counter */
    uint16_t outc;      /* outage counter */
    uint16_t slipc;     /* slip counter */
    uint16_t rejc;      /* reject counter */
"""
    _pack_ = 1
    _fields_ = [ ("time"             , gtime_t            ),
                 ("sat"              , ctypes.c_ubyte     ),
                 ("frq"              , ctypes.c_ubyte     ),
                 ("Padding_144_160_" , ctypes.c_ubyte * 2 ),
                 ("az"               , ctypes.c_float     ),
                 ("el"               , ctypes.c_float     ),
                 ("resp"             , ctypes.c_float     ),
                 ("resc"             , ctypes.c_float     ),
                 ("flag"             , ctypes.c_ubyte     ),
                 ("Padding_296_304_" , ctypes.c_ubyte * 1 ),
                 ("snr"              , ctypes.c_uint16    ),
                 ("lock"             , ctypes.c_uint16    ),
                 ("outc"             , ctypes.c_uint16    ),
                 ("slipc"            , ctypes.c_uint16    ),
                 ("rejc"             , ctypes.c_uint16    )]
    def SetConstants(self):
        """ Sets Constant fields to their default values """ 
        pass


class solstatbuf_t (my_endian):
    """
struct {        /* solution status buffer type */
    int n,nmax;         /* number of solution/max number of buffer */
    solstat_t *data;    /* solution status data */
"""
    _pack_ = 1
    _fields_ = [ ("n"    , ctypes.c_int32           ),
                 ("nmax" , ctypes.c_int32           ),
                 ("data" , ctypes.POINTER(solstat_t ) )]
    def SetConstants(self):
        """ Sets Constant fields to their default values """ 
        pass


class rtcm_t (my_endian):
    """
struct {        /* RTCM control struct type */
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
    char msmtype[7][128]; /* msm signal types */
    int obsflag;        /* obs data complete flag (1:ok,0:not complete) */
    int ephsat;         /* input ephemeris satellite number */
    int ephset;         /* input ephemeris set (0-1) */
    double cp[MAXSAT][NFREQ+NEXOBS]; /* carrier-phase measurement */
    uint16_t lock[MAXSAT][NFREQ+NEXOBS]; /* lock time */
    uint16_t loss[MAXSAT][NFREQ+NEXOBS]; /* loss of lock count */
    gtime_t lltime[MAXSAT][NFREQ+NEXOBS]; /* last lock time */
    int nbyte;          /* number of bytes in message buffer */ 
    int nbit;           /* number of bits in word buffer */ 
    int len;            /* message length (bytes) */
    uint8_t buff[1200]; /* message buffer */
    uint32_t word;      /* word buffer for rtcm 2 */
    uint32_t nmsg2[100]; /* message count of RTCM 2 (1-99:1-99,0:other) */
    uint32_t nmsg3[400]; /* message count of RTCM 3 (1-299:1001-1299,300-329:4070-4099,0:ohter) */
    char opt[256];      /* RTCM dependent options */
"""
    _pack_ = 1
    _fields_ = [ ("staid"                    , ctypes.c_int32          ),
                 ("stah"                     , ctypes.c_int32          ),
                 ("seqno"                    , ctypes.c_int32          ),
                 ("outtype"                  , ctypes.c_int32          ),
                 ("time"                     , gtime_t                 ),
                 ("time_s"                   , gtime_t                 ),
                 ("obs"                      , obs_t                   ),
                 ("nav"                      , nav_t                   ),
                 ("sta"                      , sta_t                   ),
                 ("dgps"                     , ctypes.POINTER(dgps_t   ) ),
                 ("ssr"                      , ssr_t            * 71   ),
                 ("msg"                      , ctypes.c_char    * 128  ),
                 ("msgtype"                  , ctypes.c_char    * 256  ),
                 ("msmtype"                  , (ctypes.c_char   * 128  ) * 7 ),
                 ("obsflag"                  , ctypes.c_int32          ),
                 ("ephsat"                   , ctypes.c_int32          ),
                 ("ephset"                   , ctypes.c_int32          ),
                 ("Padding_2695712_2695744_" , ctypes.c_ubyte   * 4    ),
                 ("cp"                       , (ctypes.c_double * 3    ) * 71 ),
                 ("lock"                     , (ctypes.c_uint16 * 3    ) * 71 ),
                 ("loss"                     , (ctypes.c_uint16 * 3    ) * 71 ),
                 ("Padding_2716192_2716224_" , ctypes.c_ubyte   * 4    ),
                 ("lltime"                   , (gtime_t         * 3    ) * 71 ),
                 ("nbyte"                    , ctypes.c_int32          ),
                 ("nbit"                     , ctypes.c_int32          ),
                 ("len"                      , ctypes.c_int32          ),
                 ("buff"                     , ctypes.c_ubyte   * 1200 ),
                 ("word"                     , ctypes.c_uint32         ),
                 ("nmsg2"                    , ctypes.c_uint32  * 100  ),
                 ("nmsg3"                    , ctypes.c_uint32  * 400  ),
                 ("opt"                      , ctypes.c_char    * 256  )]
    def SetConstants(self):
        """ Sets Constant fields to their default values """ 
        pass


class rnxctr_t (my_endian):
    """
struct {        /* RINEX control struct type */
    gtime_t time;       /* message time */
    double ver;         /* RINEX version */
    char   type;        /* RINEX file type ('O','N',...) */
    int    sys;         /* navigation system */
    int    tsys;        /* time system */
    char   tobs[8][MAXOBSTYPE][4]; /* rinex obs types */
    obs_t  obs;         /* observation data */
    nav_t  nav;         /* navigation data */
    sta_t  sta;         /* station info */
    int    ephsat;      /* input ephemeris satellite number */
    int    ephset;      /* input ephemeris set (0-1) */
    char   opt[256];    /* rinex dependent options */
"""
    _pack_ = 1
    _fields_ = [ ("time"                 , gtime_t               ),
                 ("ver"                  , ctypes.c_double       ),
                 ("type"                 , ctypes.c_char         ),
                 ("Padding_200_224_"     , ctypes.c_ubyte  * 3   ),
                 ("sys"                  , ctypes.c_int32        ),
                 ("tsys"                 , ctypes.c_int32        ),
                 ("tobs"                 , ((ctypes.c_char * 4   ) * 64) * 8 ),
                 ("Padding_16672_16704_" , ctypes.c_ubyte  * 4   ),
                 ("obs"                  , obs_t                 ),
                 ("nav"                  , nav_t                 ),
                 ("sta"                  , sta_t                 ),
                 ("ephsat"               , ctypes.c_int32        ),
                 ("ephset"               , ctypes.c_int32        ),
                 ("opt"                  , ctypes.c_char   * 256 )]
    def SetConstants(self):
        """ Sets Constant fields to their default values """ 
        pass


class url_t (my_endian):
    """
struct {        /* download URL type */
    char type[32];      /* data type */
    char path[1024];    /* URL path */
    char dir [1024];    /* local directory */
    double tint;        /* time interval (s) */
"""
    _pack_ = 1
    _fields_ = [ ("type" , ctypes.c_char * 32   ),
                 ("path" , ctypes.c_char * 1024 ),
                 ("dir"  , ctypes.c_char * 1024 ),
                 ("tint" , ctypes.c_double      )]
    def SetConstants(self):
        """ Sets Constant fields to their default values """ 
        pass


class opt_t (my_endian):
    """
struct {        /* option type */
    const char *name;   /* option name */
    int format;         /* option format (0:int,1:double,2:string,3:enum) */
    void *var;          /* pointer to option variable */
    const char *comment; /* option comment/enum labels/unit */
"""
    _pack_ = 1
    _fields_ = [ ("name"            , ctypes.POINTER(ctypes.c_char   ) ),
                 ("format"          , ctypes.c_int32                 ),
                 ("Padding_96_128_" , ctypes.c_ubyte * 4             ),
                 ("var"             , ctypes.POINTER(ctypes.c_void_p ) ),
                 ("comment"         , ctypes.POINTER(ctypes.c_char   ) )]
    def SetConstants(self):
        """ Sets Constant fields to their default values """ 
        pass


class snrmask_t (my_endian):
    """
struct {        /* SNR mask type */
    int ena[2];         /* enable flag {rover,base} */
    double mask[NFREQ][9]; /* mask (dBHz) at 5,10,...85 deg */
"""
    _pack_ = 1
    _fields_ = [ ("ena"  , ctypes.c_int32   * 2 ),
                 ("mask" , (ctypes.c_double * 9 ) * 3 )]
    def SetConstants(self):
        """ Sets Constant fields to their default values """ 
        pass


class prcopt_t (my_endian):
    """
struct {        /* processing options type */
    int mode;           /* positioning mode (PMODE_???) */
    int soltype;        /* solution type (0:forward,1:backward,2:combined) */
    int nf;             /* number of frequencies (1:L1,2:L1+L2,3:L1+L2+L5) */
    int navsys;         /* navigation system */
    double elmin;       /* elevation mask angle (rad) */
    snrmask_t snrmask;  /* SNR mask */
    int sateph;         /* satellite ephemeris/clock (EPHOPT_???) */
    int modear;         /* AR mode (0:off,1:continuous,2:instantaneous,3:fix and hold,4:ppp-ar) */
    int glomodear;      /* GLONASS AR mode (0:off,1:on,2:auto cal,3:ext cal) */
    int bdsmodear;      /* BeiDou AR mode (0:off,1:on) */
    int maxout;         /* obs outage count to reset bias */
    int minlock;        /* min lock count to fix ambiguity */
    int minfix;         /* min fix count to hold ambiguity */
    int armaxiter;      /* max iteration to resolve ambiguity */
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
    double prn[6];      /* process-noise std [0]bias,[1]iono [2]trop [3]acch [4]accv [5] pos */
    double sclkstab;    /* satellite clock stability (sec/sec) */
    double thresar[8];  /* AR validation threshold */
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
    uint8_t exsats[MAXSAT]; /* excluded satellites (1:excluded,2:included) */
    int  maxaveep;      /* max averaging epoches */
    int  initrst;       /* initialize by restart */
    int  outsingle;     /* output single by dgps/float/fix/ppp outage */
    char rnxopt[2][256]; /* rinex options {rover,base} */
    int  posopt[6];     /* positioning options */
    int  syncsol;       /* solution sync mode (0:off,1:on) */
    double odisp[2][6*11]; /* ocean tide loading parameters {rov,base} */
    int  freqopt;       /* disable L2-AR */
    char pppopt[256];   /* ppp option */
"""
    _pack_ = 1
    _fields_ = [ ("mode"                 , ctypes.c_int32         ),
                 ("soltype"              , ctypes.c_int32         ),
                 ("nf"                   , ctypes.c_int32         ),
                 ("navsys"               , ctypes.c_int32         ),
                 ("elmin"                , ctypes.c_double        ),
                 ("snrmask"              , snrmask_t              ),
                 ("sateph"               , ctypes.c_int32         ),
                 ("modear"               , ctypes.c_int32         ),
                 ("glomodear"            , ctypes.c_int32         ),
                 ("bdsmodear"            , ctypes.c_int32         ),
                 ("maxout"               , ctypes.c_int32         ),
                 ("minlock"              , ctypes.c_int32         ),
                 ("minfix"               , ctypes.c_int32         ),
                 ("armaxiter"            , ctypes.c_int32         ),
                 ("ionoopt"              , ctypes.c_int32         ),
                 ("tropopt"              , ctypes.c_int32         ),
                 ("dynamics"             , ctypes.c_int32         ),
                 ("tidecorr"             , ctypes.c_int32         ),
                 ("niter"                , ctypes.c_int32         ),
                 ("codesmooth"           , ctypes.c_int32         ),
                 ("intpref"              , ctypes.c_int32         ),
                 ("sbascorr"             , ctypes.c_int32         ),
                 ("sbassatsel"           , ctypes.c_int32         ),
                 ("rovpos"               , ctypes.c_int32         ),
                 ("refpos"               , ctypes.c_int32         ),
                 ("Padding_2592_2624_"   , ctypes.c_ubyte   * 4   ),
                 ("eratio"               , ctypes.c_double  * 3   ),
                 ("err"                  , ctypes.c_double  * 5   ),
                 ("std"                  , ctypes.c_double  * 3   ),
                 ("prn"                  , ctypes.c_double  * 6   ),
                 ("sclkstab"             , ctypes.c_double        ),
                 ("thresar"              , ctypes.c_double  * 8   ),
                 ("elmaskar"             , ctypes.c_double        ),
                 ("elmaskhold"           , ctypes.c_double        ),
                 ("thresslip"            , ctypes.c_double        ),
                 ("maxtdiff"             , ctypes.c_double        ),
                 ("maxinno"              , ctypes.c_double        ),
                 ("maxgdop"              , ctypes.c_double        ),
                 ("baseline"             , ctypes.c_double  * 2   ),
                 ("ru"                   , ctypes.c_double  * 3   ),
                 ("rb"                   , ctypes.c_double  * 3   ),
                 ("anttype"              , (ctypes.c_char   * 64  ) * 2 ),
                 ("antdel"               , (ctypes.c_double * 3   ) * 2 ),
                 ("pcvr"                 , pcv_t            * 2   ),
                 ("exsats"               , ctypes.c_ubyte   * 71  ),
                 ("Padding_18296_18304_" , ctypes.c_ubyte   * 1   ),
                 ("maxaveep"             , ctypes.c_int32         ),
                 ("initrst"              , ctypes.c_int32         ),
                 ("outsingle"            , ctypes.c_int32         ),
                 ("rnxopt"               , (ctypes.c_char   * 256 ) * 2 ),
                 ("posopt"               , ctypes.c_int32   * 6   ),
                 ("syncsol"              , ctypes.c_int32         ),
                 ("odisp"                , (ctypes.c_double * 66  ) * 2 ),
                 ("freqopt"              , ctypes.c_int32         ),
                 ("pppopt"               , ctypes.c_char    * 256 ),
                 ("Padding_33248_"       , ctypes.c_ubyte   * 4   )]
    def SetConstants(self):
        """ Sets Constant fields to their default values """ 
        pass


class solopt_t (my_endian):
    """
struct {        /* solution options type */
    int posf;           /* solution format (SOLF_???) */
    int times;          /* time system (TIMES_???) */
    int timef;          /* time format (0:sssss.s,1:yyyy/mm/dd hh:mm:ss.s) */
    int timeu;          /* time digits under decimal point */
    int degf;           /* latitude/longitude format (0:ddd.ddd,1:ddd mm ss) */
    int outhead;        /* output header (0:no,1:yes) */
    int outopt;         /* output processing options (0:no,1:yes) */
    int outvel;         /* output velocity options (0:no,1:yes) */
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
    double maxsolstd;   /* max std-dev for solution output (m) (0:all) */
"""
    _pack_ = 1
    _fields_ = [ ("posf"      , ctypes.c_int32       ),
                 ("times"     , ctypes.c_int32       ),
                 ("timef"     , ctypes.c_int32       ),
                 ("timeu"     , ctypes.c_int32       ),
                 ("degf"      , ctypes.c_int32       ),
                 ("outhead"   , ctypes.c_int32       ),
                 ("outopt"    , ctypes.c_int32       ),
                 ("outvel"    , ctypes.c_int32       ),
                 ("datum"     , ctypes.c_int32       ),
                 ("height"    , ctypes.c_int32       ),
                 ("geoid"     , ctypes.c_int32       ),
                 ("solstatic" , ctypes.c_int32       ),
                 ("sstat"     , ctypes.c_int32       ),
                 ("trace"     , ctypes.c_int32       ),
                 ("nmeaintv"  , ctypes.c_double * 2  ),
                 ("sep"       , ctypes.c_char   * 64 ),
                 ("prog"      , ctypes.c_char   * 64 ),
                 ("maxsolstd" , ctypes.c_double      )]
    def SetConstants(self):
        """ Sets Constant fields to their default values """ 
        pass


class filopt_t (my_endian):
    """
struct {        /* file options type */
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
"""
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
        """ Sets Constant fields to their default values """ 
        pass


class rnxopt_t (my_endian):
    """
struct {        /* RINEX options type */
    gtime_t ts,te;      /* time start/end */
    double tint;        /* time interval (s) */
    double ttol;        /* time tolerance (s) */
    double tunit;       /* time unit for multiple-session (s) */
    int rnxver;         /* RINEX version (x100) */
    int navsys;         /* navigation system */
    int obstype;        /* observation type */
    int freqtype;       /* frequency type */
    char mask[7][64];   /* code mask {GPS,GLO,GAL,QZS,SBS,CMP,IRN} */
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
    double glo_cp_bias[4]; /* GLONASS code-phase biases (m) */
    char comment[MAXCOMMENT][64]; /* comments */
    char rcvopt[256];   /* receiver dependent options */
    uint8_t exsats[MAXSAT]; /* excluded satellites */
    int glofcn[32];     /* glonass fcn+8 */
    int outiono;        /* output iono correction */
    int outtime;        /* output time system correction */
    int outleaps;       /* output leap seconds */
    int autopos;        /* auto approx position */
    int phshift;        /* phase shift correction */
    int halfcyc;        /* half cycle correction */
    int sep_nav;        /* separated nav files */
    gtime_t tstart;     /* first obs time */
    gtime_t tend;       /* last obs time */
    gtime_t trtcm;      /* approx log start time for rtcm */
    char tobs[7][MAXOBSTYPE][4]; /* obs types {GPS,GLO,GAL,QZS,SBS,CMP,IRN} */
    double shift[7][MAXOBSTYPE]; /* phase shift (cyc) {GPS,GLO,GAL,QZS,SBS,CMP,IRN} */
    int nobs[7];        /* number of obs types {GPS,GLO,GAL,QZS,SBS,CMP,IRN} */
"""
    _pack_ = 1
    _fields_ = [ ("ts"                   , gtime_t                ),
                 ("te"                   , gtime_t                ),
                 ("tint"                 , ctypes.c_double        ),
                 ("ttol"                 , ctypes.c_double        ),
                 ("tunit"                , ctypes.c_double        ),
                 ("rnxver"               , ctypes.c_int32         ),
                 ("navsys"               , ctypes.c_int32         ),
                 ("obstype"              , ctypes.c_int32         ),
                 ("freqtype"             , ctypes.c_int32         ),
                 ("mask"                 , (ctypes.c_char   * 64  ) * 7 ),
                 ("staid"                , ctypes.c_char    * 32  ),
                 ("prog"                 , ctypes.c_char    * 32  ),
                 ("runby"                , ctypes.c_char    * 32  ),
                 ("marker"               , ctypes.c_char    * 64  ),
                 ("markerno"             , ctypes.c_char    * 32  ),
                 ("markertype"           , ctypes.c_char    * 32  ),
                 ("name"                 , (ctypes.c_char   * 32  ) * 2 ),
                 ("rec"                  , (ctypes.c_char   * 32  ) * 3 ),
                 ("ant"                  , (ctypes.c_char   * 32  ) * 3 ),
                 ("apppos"               , ctypes.c_double  * 3   ),
                 ("antdel"               , ctypes.c_double  * 3   ),
                 ("glo_cp_bias"          , ctypes.c_double  * 4   ),
                 ("comment"              , (ctypes.c_char   * 64  ) * 100 ),
                 ("rcvopt"               , ctypes.c_char    * 256 ),
                 ("exsats"               , ctypes.c_ubyte   * 71  ),
                 ("Padding_62456_62464_" , ctypes.c_ubyte   * 1   ),
                 ("glofcn"               , ctypes.c_int32   * 32  ),
                 ("outiono"              , ctypes.c_int32         ),
                 ("outtime"              , ctypes.c_int32         ),
                 ("outleaps"             , ctypes.c_int32         ),
                 ("autopos"              , ctypes.c_int32         ),
                 ("phshift"              , ctypes.c_int32         ),
                 ("halfcyc"              , ctypes.c_int32         ),
                 ("sep_nav"              , ctypes.c_int32         ),
                 ("Padding_63712_63744_" , ctypes.c_ubyte   * 4   ),
                 ("tstart"               , gtime_t                ),
                 ("tend"                 , gtime_t                ),
                 ("trtcm"                , gtime_t                ),
                 ("tobs"                 , ((ctypes.c_char  * 4   ) * 64) * 7 ),
                 ("shift"                , (ctypes.c_double * 64  ) * 7 ),
                 ("nobs"                 , ctypes.c_int32   * 7   ),
                 ("Padding_107360_"      , ctypes.c_ubyte   * 4   )]
    def SetConstants(self):
        """ Sets Constant fields to their default values """ 
        pass


class ssat_t (my_endian):
    """
struct {        /* satellite status type */
    uint8_t sys;        /* navigation system */
    uint8_t vs;         /* valid satellite flag single */
    double azel[2];     /* azimuth/elevation angles {az,el} (rad) */
    double resp[NFREQ]; /* residuals of pseudorange (m) */
    double resc[NFREQ]; /* residuals of carrier-phase (m) */
    uint8_t vsat[NFREQ]; /* valid satellite flag */
    uint16_t snr[NFREQ]; /* signal strength (*SNR_UNIT dBHz) */
    uint8_t fix [NFREQ]; /* ambiguity fix flag (1:fix,2:float,3:hold) */
    uint8_t slip[NFREQ]; /* cycle-slip flag */
    uint8_t half[NFREQ]; /* half-cycle valid flag */
    int lock [NFREQ];   /* lock counter of phase */
    uint32_t outc [NFREQ]; /* obs outage counter of phase */
    uint32_t slipc[NFREQ]; /* cycle-slip counter */
    uint32_t rejc [NFREQ]; /* reject counter */
    double gf[NFREQ-1]; /* geometry-free phase (m) */
    double mw[NFREQ-1]; /* MW-LC (m) */
    double phw;         /* phase windup (cycle) */
    gtime_t pt[2][NFREQ]; /* previous carrier-phase time */
    double ph[2][NFREQ]; /* previous carrier-phase observable (cycle) */
"""
    _pack_ = 1
    _fields_ = [ ("sys"                , ctypes.c_ubyte       ),
                 ("vs"                 , ctypes.c_ubyte       ),
                 ("Padding_16_64_"     , ctypes.c_ubyte   * 6 ),
                 ("azel"               , ctypes.c_double  * 2 ),
                 ("resp"               , ctypes.c_double  * 3 ),
                 ("resc"               , ctypes.c_double  * 3 ),
                 ("vsat"               , ctypes.c_ubyte   * 3 ),
                 ("Padding_600_608_"   , ctypes.c_ubyte   * 1 ),
                 ("snr"                , ctypes.c_uint16  * 3 ),
                 ("fix"                , ctypes.c_ubyte   * 3 ),
                 ("slip"               , ctypes.c_ubyte   * 3 ),
                 ("half"               , ctypes.c_ubyte   * 3 ),
                 ("Padding_728_736_"   , ctypes.c_ubyte   * 1 ),
                 ("lock"               , ctypes.c_int32   * 3 ),
                 ("outc"               , ctypes.c_uint32  * 3 ),
                 ("slipc"              , ctypes.c_uint32  * 3 ),
                 ("rejc"               , ctypes.c_uint32  * 3 ),
                 ("Padding_1120_1152_" , ctypes.c_ubyte   * 4 ),
                 ("gf"                 , ctypes.c_double  * 2 ),
                 ("mw"                 , ctypes.c_double  * 2 ),
                 ("phw"                , ctypes.c_double      ),
                 ("pt"                 , (gtime_t         * 3 ) * 2 ),
                 ("ph"                 , (ctypes.c_double * 3 ) * 2 )]
    def SetConstants(self):
        """ Sets Constant fields to their default values """ 
        pass


class ambc_t (my_endian):
    """
struct {        /* ambiguity control type */
    gtime_t epoch[4];   /* last epoch */
    int n[4];           /* number of epochs */
    double LC [4];      /* linear combination average */
    double LCv[4];      /* linear combination variance */
    int fixcnt;         /* fix count */
    char flags[MAXSAT]; /* fix flags */
"""
    _pack_ = 1
    _fields_ = [ ("epoch"         , gtime_t         * 4  ),
                 ("n"             , ctypes.c_int32  * 4  ),
                 ("LC"            , ctypes.c_double * 4  ),
                 ("LCv"           , ctypes.c_double * 4  ),
                 ("fixcnt"        , ctypes.c_int32       ),
                 ("flags"         , ctypes.c_char   * 71 ),
                 ("Padding_1752_" , ctypes.c_ubyte  * 5  )]
    def SetConstants(self):
        """ Sets Constant fields to their default values """ 
        pass


class rtk_t (my_endian):
    """
struct {        /* RTK control/result type */
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
"""
    _pack_ = 1
    _fields_ = [ ("sol"                    , sol_t                          ),
                 ("rb"                     , ctypes.c_double * 6            ),
                 ("nx"                     , ctypes.c_int32                 ),
                 ("na"                     , ctypes.c_int32                 ),
                 ("tt"                     , ctypes.c_double                ),
                 ("x"                      , ctypes.POINTER(ctypes.c_double ) ),
                 ("P"                      , ctypes.POINTER(ctypes.c_double ) ),
                 ("xa"                     , ctypes.POINTER(ctypes.c_double ) ),
                 ("Pa"                     , ctypes.POINTER(ctypes.c_double ) ),
                 ("nfix"                   , ctypes.c_int32                 ),
                 ("Padding_2208_2240_"     , ctypes.c_ubyte  * 4            ),
                 ("ambc"                   , ambc_t          * 71           ),
                 ("ssat"                   , ssat_t          * 71           ),
                 ("neb"                    , ctypes.c_int32                 ),
                 ("errbuf"                 , ctypes.c_char   * 4096         ),
                 ("Padding_348576_348608_" , ctypes.c_ubyte  * 4            ),
                 ("opt"                    , prcopt_t                       )]
    def SetConstants(self):
        """ Sets Constant fields to their default values """ 
        pass


class raw_t (my_endian):
    """
struct {        /* receiver raw data control type */
    gtime_t time;       /* message time */
    gtime_t tobs[MAXSAT][NFREQ+NEXOBS]; /* observation data time */
    obs_t obs;          /* observation data */
    obs_t obuf;         /* observation data buffer */
    nav_t nav;          /* satellite ephemerides */
    sta_t sta;          /* station parameters */
    int ephsat;         /* update satelle of ephemeris (0:no satellite) */
    int ephset;         /* update set of ephemeris (0-1) */
    sbsmsg_t sbsmsg;    /* SBAS message */
    char msgtype[256];  /* last message type */
    uint8_t subfrm[MAXSAT][380]; /* subframe buffer */
    double lockt[MAXSAT][NFREQ+NEXOBS]; /* lock time (s) */
    double icpp[MAXSAT],off[MAXSAT],icpc; /* carrier params for ss2 */
    double prCA[MAXSAT],dpCA[MAXSAT]; /* L1/CA pseudrange/doppler for javad */
    uint8_t halfc[MAXSAT][NFREQ+NEXOBS]; /* half-cycle add flag */
    char freqn[MAXOBS]; /* frequency number for javad */
    int nbyte;          /* number of bytes in message buffer */ 
    int len;            /* message length (bytes) */
    int iod;            /* issue of data */
    int tod;            /* time of day (ms) */
    int tbase;          /* time base (0:gpst,1:utc(usno),2:glonass,3:utc(su) */
    int flag;           /* general purpose flag */
    int outtype;        /* output message type */
    uint8_t buff[MAXRAWLEN]; /* message buffer */
    char opt[256];      /* receiver dependent options */
    int format;         /* receiver stream format */
    void *rcv_data;     /* receiver dependent data */
"""
    _pack_ = 1
    _fields_ = [ ("time"                     , gtime_t                        ),
                 ("tobs"                     , (gtime_t         * 3           ) * 71 ),
                 ("obs"                      , obs_t                          ),
                 ("obuf"                     , obs_t                          ),
                 ("nav"                      , nav_t                          ),
                 ("sta"                      , sta_t                          ),
                 ("ephsat"                   , ctypes.c_int32                 ),
                 ("ephset"                   , ctypes.c_int32                 ),
                 ("sbsmsg"                   , sbsmsg_t                       ),
                 ("msgtype"                  , ctypes.c_char    * 256         ),
                 ("subfrm"                   , (ctypes.c_ubyte  * 380         ) * 71 ),
                 ("Padding_2149152_2149184_" , ctypes.c_ubyte   * 4           ),
                 ("lockt"                    , (ctypes.c_double * 3           ) * 71 ),
                 ("icpp"                     , ctypes.c_double  * 71          ),
                 ("off"                      , ctypes.c_double  * 71          ),
                 ("icpc"                     , ctypes.c_double                ),
                 ("prCA"                     , ctypes.c_double  * 71          ),
                 ("dpCA"                     , ctypes.c_double  * 71          ),
                 ("halfc"                    , (ctypes.c_ubyte  * 3           ) * 71 ),
                 ("freqn"                    , ctypes.c_char    * 96          ),
                 ("Padding_2183528_2183552_" , ctypes.c_ubyte   * 3           ),
                 ("nbyte"                    , ctypes.c_int32                 ),
                 ("len"                      , ctypes.c_int32                 ),
                 ("iod"                      , ctypes.c_int32                 ),
                 ("tod"                      , ctypes.c_int32                 ),
                 ("tbase"                    , ctypes.c_int32                 ),
                 ("flag"                     , ctypes.c_int32                 ),
                 ("outtype"                  , ctypes.c_int32                 ),
                 ("buff"                     , ctypes.c_ubyte   * 16384       ),
                 ("opt"                      , ctypes.c_char    * 256         ),
                 ("format"                   , ctypes.c_int32                 ),
                 ("rcv_data"                 , ctypes.POINTER(ctypes.c_void_p ) )]
    def SetConstants(self):
        """ Sets Constant fields to their default values """ 
        pass


class _opaque_pthread_mutex_t (my_endian):
    """
_opaque_pthread_mutex_t {
	long __sig;
	char __opaque[__PTHREAD_MUTEX_SIZE__];
"""
    _pack_ = 1
    _fields_ = [ ("__sig"    , ctypes.c_int64     ),
                 ("__opaque" , ctypes.c_char * 56 )]
    def SetConstants(self):
        """ Sets Constant fields to their default values """ 
        pass


class stream_t (my_endian):
    """
struct {        /* stream type */
    int type;           /* type (STR_???) */
    int mode;           /* mode (STR_MODE_?) */
    int state;          /* state (-1:error,0:close,1:open) */
    uint32_t inb,inr;   /* input bytes/rate */
    uint32_t outb,outr; /* output bytes/rate */
    uint32_t tick_i;    /* input tick tick */
    uint32_t tick_o;    /* output tick */
    uint32_t tact;      /* active tick */
    uint32_t inbt,outbt; /* input/output bytes at tick */
    rtklock_t lock;        /* lock flag */
    void *port;         /* type dependent port control struct */
    char path[MAXSTRPATH]; /* stream path */
    char msg [MAXSTRMSG];  /* stream message */
"""
    _pack_ = 1
    _fields_ = [ ("type"   , ctypes.c_int32                 ),
                 ("mode"   , ctypes.c_int32                 ),
                 ("state"  , ctypes.c_int32                 ),
                 ("inb"    , ctypes.c_uint32                ),
                 ("inr"    , ctypes.c_uint32                ),
                 ("outb"   , ctypes.c_uint32                ),
                 ("outr"   , ctypes.c_uint32                ),
                 ("tick_i" , ctypes.c_uint32                ),
                 ("tick_o" , ctypes.c_uint32                ),
                 ("tact"   , ctypes.c_uint32                ),
                 ("inbt"   , ctypes.c_uint32                ),
                 ("outbt"  , ctypes.c_uint32                ),
                 ("lock"   , _opaque_pthread_mutex_t        ),
                 ("port"   , ctypes.POINTER(ctypes.c_void_p ) ),
                 ("path"   , ctypes.c_char * 1024           ),
                 ("msg"    , ctypes.c_char * 1024           )]
    def SetConstants(self):
        """ Sets Constant fields to their default values """ 
        pass


class strconv_t (my_endian):
    """
struct {        /* stream converter type */
    int itype,otype;    /* input and output stream type */
    int nmsg;           /* number of output messages */
    int msgs[32];       /* output message types */
    double tint[32];    /* output message intervals (s) */
    uint32_t tick[32];  /* cycle tick of output message */
    int ephsat[32];     /* satellites of output ephemeris */
    int stasel;         /* station info selection (0:remote,1:local) */
    rtcm_t rtcm;        /* rtcm input data buffer */
    raw_t raw;          /* raw  input data buffer */
    rtcm_t out;         /* rtcm output data buffer */
"""
    _pack_ = 1
    _fields_ = [ ("itype"              , ctypes.c_int32       ),
                 ("otype"              , ctypes.c_int32       ),
                 ("nmsg"               , ctypes.c_int32       ),
                 ("msgs"               , ctypes.c_int32  * 32 ),
                 ("Padding_1120_1152_" , ctypes.c_ubyte  * 4  ),
                 ("tint"               , ctypes.c_double * 32 ),
                 ("tick"               , ctypes.c_uint32 * 32 ),
                 ("ephsat"             , ctypes.c_int32  * 32 ),
                 ("stasel"             , ctypes.c_int32       ),
                 ("Padding_5280_5312_" , ctypes.c_ubyte  * 4  ),
                 ("rtcm"               , rtcm_t               ),
                 ("raw"                , raw_t                ),
                 ("out"                , rtcm_t               )]
    def SetConstants(self):
        """ Sets Constant fields to their default values """ 
        pass


class strsvr_t (my_endian):
    """
struct {        /* stream server type */
    int state;          /* server state (0:stop,1:running) */
    int cycle;          /* server cycle (ms) */
    int buffsize;       /* input/monitor buffer size (bytes) */
    int nmeacycle;      /* NMEA request cycle (ms) (0:no) */
    int relayback;      /* relay back of output streams (0:no) */
    int nstr;           /* number of streams (1 input + (nstr-1) outputs */
    int npb;            /* data length in peek buffer (bytes) */
    char cmds_periodic[16][MAXRCVCMD]; /* periodic commands */
    double nmeapos[3];  /* NMEA request position (ecef) (m) */
    uint8_t *buff;      /* input buffers */
    uint8_t *pbuf;      /* peek buffer */
    uint32_t tick;      /* start tick */
    stream_t stream[16]; /* input/output streams */
    stream_t strlog[16]; /* return log streams */
    strconv_t *conv[16]; /* stream converter */
    rtkthread_t thread;    /* server thread */
    rtklock_t lock;        /* lock flag */
"""
    _pack_ = 1
    _fields_ = [ ("state"                  , ctypes.c_int32                ),
                 ("cycle"                  , ctypes.c_int32                ),
                 ("buffsize"               , ctypes.c_int32                ),
                 ("nmeacycle"              , ctypes.c_int32                ),
                 ("relayback"              , ctypes.c_int32                ),
                 ("nstr"                   , ctypes.c_int32                ),
                 ("npb"                    , ctypes.c_int32                ),
                 ("cmds_periodic"          , (ctypes.c_char  * 4096        ) * 16 ),
                 ("Padding_524512_524544_" , ctypes.c_ubyte  * 4           ),
                 ("nmeapos"                , ctypes.c_double * 3           ),
                 ("buff"                   , ctypes.POINTER(ctypes.c_ubyte ) ),
                 ("pbuf"                   , ctypes.POINTER(ctypes.c_ubyte ) ),
                 ("tick"                   , ctypes.c_uint32               ),
                 ("Padding_524896_524928_" , ctypes.c_ubyte  * 4           ),
                 ("stream"                 , stream_t        * 16          ),
                 ("strlog"                 , stream_t        * 16          ),
                 ("conv"                   , ctypes.c_void_p * 16          ),
                 ("thread"                 , ctypes.c_void_p               ),
                 ("lock"                   , _opaque_pthread_mutex_t       )]
    def SetConstants(self):
        """ Sets Constant fields to their default values """ 
        pass


class rtksvr_t (my_endian):
    """
struct {        /* RTK server type */
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
    uint8_t *buff[3];   /* input buffers {rov,base,corr} */
    uint8_t *sbuf[2];   /* output buffers {sol1,sol2} */
    uint8_t *pbuf[3];   /* peek buffers {rov,base,corr} */
    sol_t solbuf[MAXSOLBUF]; /* solution buffer */
    uint32_t nmsg[3][10]; /* input message counts */
    raw_t  raw [3];     /* receiver raw control {rov,base,corr} */
    rtcm_t rtcm[3];     /* RTCM control {rov,base,corr} */
    gtime_t ftime[3];   /* download time {rov,base,corr} */
    char files[3][MAXSTRPATH]; /* download paths {rov,base,corr} */
    obs_t obs[3][MAXOBSBUF]; /* observation data {rov,base,corr} */
    nav_t nav;          /* navigation data */
    sbsmsg_t sbsmsg[MAXSBSMSG]; /* SBAS message buffer */
    stream_t stream[8]; /* streams {rov,base,corr,sol1,sol2,logr,logb,logc} */
    stream_t *moni;     /* monitor stream */
    uint32_t tick;      /* start tick */
    rtkthread_t thread;    /* server thread */
    int cputime;        /* CPU time (ms) for a processing cycle */
    int prcout;         /* missing observation data count */
    int nave;           /* number of averaging base pos */
    double rb_ave[3];   /* averaging base pos */
    char cmds_periodic[3][MAXRCVCMD]; /* periodic commands */
    char cmd_reset[MAXRCVCMD]; /* reset command */
    double bl_reset;    /* baseline length to reset (km) */
    rtklock_t lock;        /* lock flag */
"""
    _pack_ = 1
    _fields_ = [ ("state"                      , ctypes.c_int32          ),
                 ("cycle"                      , ctypes.c_int32          ),
                 ("nmeacycle"                  , ctypes.c_int32          ),
                 ("nmeareq"                    , ctypes.c_int32          ),
                 ("nmeapos"                    , ctypes.c_double  * 3    ),
                 ("buffsize"                   , ctypes.c_int32          ),
                 ("format"                     , ctypes.c_int32   * 3    ),
                 ("solopt"                     , solopt_t         * 2    ),
                 ("navsel"                     , ctypes.c_int32          ),
                 ("nsbs"                       , ctypes.c_int32          ),
                 ("nsol"                       , ctypes.c_int32          ),
                 ("Padding_3872_3904_"         , ctypes.c_ubyte   * 4    ),
                 ("rtk"                        , rtk_t                   ),
                 ("nb"                         , ctypes.c_int32   * 3    ),
                 ("nsb"                        , ctypes.c_int32   * 2    ),
                 ("npb"                        , ctypes.c_int32   * 3    ),
                 ("buff"                       , ctypes.c_void_p  * 3    ),
                 ("sbuf"                       , ctypes.c_void_p  * 2    ),
                 ("pbuf"                       , ctypes.c_void_p  * 3    ),
                 ("solbuf"                     , sol_t            * 256  ),
                 ("nmsg"                       , (ctypes.c_uint32 * 10   ) * 3 ),
                 ("raw"                        , raw_t            * 3    ),
                 ("rtcm"                       , rtcm_t           * 3    ),
                 ("ftime"                      , gtime_t          * 3    ),
                 ("files"                      , (ctypes.c_char   * 1024 ) * 3 ),
                 ("obs"                        , (obs_t           * 128  ) * 3 ),
                 ("nav"                        , nav_t                   ),
                 ("sbsmsg"                     , sbsmsg_t         * 32   ),
                 ("stream"                     , stream_t         * 8    ),
                 ("moni"                       , ctypes.POINTER(stream_t ) ),
                 ("tick"                       , ctypes.c_uint32         ),
                 ("Padding_18134688_18134720_" , ctypes.c_ubyte   * 4    ),
                 ("thread"                     , ctypes.c_void_p         ),
                 ("cputime"                    , ctypes.c_int32          ),
                 ("prcout"                     , ctypes.c_int32          ),
                 ("nave"                       , ctypes.c_int32          ),
                 ("Padding_18134880_18134912_" , ctypes.c_ubyte   * 4    ),
                 ("rb_ave"                     , ctypes.c_double  * 3    ),
                 ("cmds_periodic"              , (ctypes.c_char   * 4096 ) * 3 ),
                 ("cmd_reset"                  , ctypes.c_char    * 4096 ),
                 ("bl_reset"                   , ctypes.c_double         ),
                 ("lock"                       , _opaque_pthread_mutex_t )]
    def SetConstants(self):
        """ Sets Constant fields to their default values """ 
        pass


class gis_pnt_t (my_endian):
    """
struct {        /* GIS data point type */
    double pos[3];      /* point data {lat,lon,height} (rad,m) */
"""
    _pack_ = 1
    _fields_ = [ ("pos" , ctypes.c_double * 3 )]
    def SetConstants(self):
        """ Sets Constant fields to their default values """ 
        pass


class gis_poly_t (my_endian):
    """
struct {        /* GIS data polyline type */
    int npnt;           /* number of points */
    double bound[4];    /* boundary {lat0,lat1,lon0,lon1} */
    double *pos;        /* position data (3 x npnt) */
"""
    _pack_ = 1
    _fields_ = [ ("npnt"           , ctypes.c_int32                 ),
                 ("Padding_32_64_" , ctypes.c_ubyte  * 4            ),
                 ("bound"          , ctypes.c_double * 4            ),
                 ("pos"            , ctypes.POINTER(ctypes.c_double ) )]
    def SetConstants(self):
        """ Sets Constant fields to their default values """ 
        pass


class gis_polygon_t (my_endian):
    """
struct {        /* GIS data polygon type */
    int npnt;           /* number of points */
    double bound[4];    /* boundary {lat0,lat1,lon0,lon1} */
    double *pos;        /* position data (3 x npnt) */
"""
    _pack_ = 1
    _fields_ = [ ("npnt"           , ctypes.c_int32                 ),
                 ("Padding_32_64_" , ctypes.c_ubyte  * 4            ),
                 ("bound"          , ctypes.c_double * 4            ),
                 ("pos"            , ctypes.POINTER(ctypes.c_double ) )]
    def SetConstants(self):
        """ Sets Constant fields to their default values """ 
        pass


class prcopt_default (my_endian):
    """
struct {        /* processing options type */
    int mode;           /* positioning mode (PMODE_???) */
    int soltype;        /* solution type (0:forward,1:backward,2:combined) */
    int nf;             /* number of frequencies (1:L1,2:L1+L2,3:L1+L2+L5) */
    int navsys;         /* navigation system */
    double elmin;       /* elevation mask angle (rad) */
    snrmask_t snrmask;  /* SNR mask */
    int sateph;         /* satellite ephemeris/clock (EPHOPT_???) */
    int modear;         /* AR mode (0:off,1:continuous,2:instantaneous,3:fix and hold,4:ppp-ar) */
    int glomodear;      /* GLONASS AR mode (0:off,1:on,2:auto cal,3:ext cal) */
    int bdsmodear;      /* BeiDou AR mode (0:off,1:on) */
    int maxout;         /* obs outage count to reset bias */
    int minlock;        /* min lock count to fix ambiguity */
    int minfix;         /* min fix count to hold ambiguity */
    int armaxiter;      /* max iteration to resolve ambiguity */
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
    double prn[6];      /* process-noise std [0]bias,[1]iono [2]trop [3]acch [4]accv [5] pos */
    double sclkstab;    /* satellite clock stability (sec/sec) */
    double thresar[8];  /* AR validation threshold */
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
    uint8_t exsats[MAXSAT]; /* excluded satellites (1:excluded,2:included) */
    int  maxaveep;      /* max averaging epoches */
    int  initrst;       /* initialize by restart */
    int  outsingle;     /* output single by dgps/float/fix/ppp outage */
    char rnxopt[2][256]; /* rinex options {rover,base} */
    int  posopt[6];     /* positioning options */
    int  syncsol;       /* solution sync mode (0:off,1:on) */
    double odisp[2][6*11]; /* ocean tide loading parameters {rov,base} */
    int  freqopt;       /* disable L2-AR */
    char pppopt[256];   /* ppp option */
"""
    _pack_ = 1
    _fields_ = [ ("mode"                 , ctypes.c_int32         ),
                 ("soltype"              , ctypes.c_int32         ),
                 ("nf"                   , ctypes.c_int32         ),
                 ("navsys"               , ctypes.c_int32         ),
                 ("elmin"                , ctypes.c_double        ),
                 ("snrmask"              , snrmask_t              ),
                 ("sateph"               , ctypes.c_int32         ),
                 ("modear"               , ctypes.c_int32         ),
                 ("glomodear"            , ctypes.c_int32         ),
                 ("bdsmodear"            , ctypes.c_int32         ),
                 ("maxout"               , ctypes.c_int32         ),
                 ("minlock"              , ctypes.c_int32         ),
                 ("minfix"               , ctypes.c_int32         ),
                 ("armaxiter"            , ctypes.c_int32         ),
                 ("ionoopt"              , ctypes.c_int32         ),
                 ("tropopt"              , ctypes.c_int32         ),
                 ("dynamics"             , ctypes.c_int32         ),
                 ("tidecorr"             , ctypes.c_int32         ),
                 ("niter"                , ctypes.c_int32         ),
                 ("codesmooth"           , ctypes.c_int32         ),
                 ("intpref"              , ctypes.c_int32         ),
                 ("sbascorr"             , ctypes.c_int32         ),
                 ("sbassatsel"           , ctypes.c_int32         ),
                 ("rovpos"               , ctypes.c_int32         ),
                 ("refpos"               , ctypes.c_int32         ),
                 ("Padding_2592_2624_"   , ctypes.c_ubyte   * 4   ),
                 ("eratio"               , ctypes.c_double  * 3   ),
                 ("err"                  , ctypes.c_double  * 5   ),
                 ("std"                  , ctypes.c_double  * 3   ),
                 ("prn"                  , ctypes.c_double  * 6   ),
                 ("sclkstab"             , ctypes.c_double        ),
                 ("thresar"              , ctypes.c_double  * 8   ),
                 ("elmaskar"             , ctypes.c_double        ),
                 ("elmaskhold"           , ctypes.c_double        ),
                 ("thresslip"            , ctypes.c_double        ),
                 ("maxtdiff"             , ctypes.c_double        ),
                 ("maxinno"              , ctypes.c_double        ),
                 ("maxgdop"              , ctypes.c_double        ),
                 ("baseline"             , ctypes.c_double  * 2   ),
                 ("ru"                   , ctypes.c_double  * 3   ),
                 ("rb"                   , ctypes.c_double  * 3   ),
                 ("anttype"              , (ctypes.c_char   * 64  ) * 2 ),
                 ("antdel"               , (ctypes.c_double * 3   ) * 2 ),
                 ("pcvr"                 , pcv_t            * 2   ),
                 ("exsats"               , ctypes.c_ubyte   * 71  ),
                 ("Padding_18296_18304_" , ctypes.c_ubyte   * 1   ),
                 ("maxaveep"             , ctypes.c_int32         ),
                 ("initrst"              , ctypes.c_int32         ),
                 ("outsingle"            , ctypes.c_int32         ),
                 ("rnxopt"               , (ctypes.c_char   * 256 ) * 2 ),
                 ("posopt"               , ctypes.c_int32   * 6   ),
                 ("syncsol"              , ctypes.c_int32         ),
                 ("odisp"                , (ctypes.c_double * 66  ) * 2 ),
                 ("freqopt"              , ctypes.c_int32         ),
                 ("pppopt"               , ctypes.c_char    * 256 ),
                 ("Padding_33248_"       , ctypes.c_ubyte   * 4   )]
    def SetConstants(self):
        """ Sets Constant fields to their default values """ 
        pass


class solopt_default (my_endian):
    """
struct {        /* solution options type */
    int posf;           /* solution format (SOLF_???) */
    int times;          /* time system (TIMES_???) */
    int timef;          /* time format (0:sssss.s,1:yyyy/mm/dd hh:mm:ss.s) */
    int timeu;          /* time digits under decimal point */
    int degf;           /* latitude/longitude format (0:ddd.ddd,1:ddd mm ss) */
    int outhead;        /* output header (0:no,1:yes) */
    int outopt;         /* output processing options (0:no,1:yes) */
    int outvel;         /* output velocity options (0:no,1:yes) */
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
    double maxsolstd;   /* max std-dev for solution output (m) (0:all) */
"""
    _pack_ = 1
    _fields_ = [ ("posf"      , ctypes.c_int32       ),
                 ("times"     , ctypes.c_int32       ),
                 ("timef"     , ctypes.c_int32       ),
                 ("timeu"     , ctypes.c_int32       ),
                 ("degf"      , ctypes.c_int32       ),
                 ("outhead"   , ctypes.c_int32       ),
                 ("outopt"    , ctypes.c_int32       ),
                 ("outvel"    , ctypes.c_int32       ),
                 ("datum"     , ctypes.c_int32       ),
                 ("height"    , ctypes.c_int32       ),
                 ("geoid"     , ctypes.c_int32       ),
                 ("solstatic" , ctypes.c_int32       ),
                 ("sstat"     , ctypes.c_int32       ),
                 ("trace"     , ctypes.c_int32       ),
                 ("nmeaintv"  , ctypes.c_double * 2  ),
                 ("sep"       , ctypes.c_char   * 64 ),
                 ("prog"      , ctypes.c_char   * 64 ),
                 ("maxsolstd" , ctypes.c_double      )]
    def SetConstants(self):
        """ Sets Constant fields to their default values """ 
        pass


class __sFILE (my_endian):
    """
__sFILE {
	unsigned char *_p;	/* current position in (some) buffer */
	int	_r;		/* read space left for getc() */
	int	_w;		/* write space left for putc() */
	short	_flags;		/* flags, below; this FILE is free if 0 */
	short	_file;		/* fileno, if Unix descriptor, else -1 */
	struct	__sbuf _bf;	/* the buffer (at least 1 byte, if !NULL) */
	int	_lbfsize;	/* 0 or -_bf._size, for inline putc */

	/* operations */
	void	*_cookie;	/* cookie passed to io functions */
	int	(* _Nullable _close)(void *);
	int	(* _Nullable _read) (void *, char *, int);
	fpos_t	(* _Nullable _seek) (void *, fpos_t, int);
	int	(* _Nullable _write)(void *, const char *, int);

	/* separate buffer for long sequences of ungetc() */
	struct	__sbuf _ub;	/* ungetc buffer */
	struct __sFILEX *_extra; /* additions to FILE to not break ABI */
	int	_ur;		/* saved _r when _r is counting ungetc data */

	/* tricks to meet minimum requirements even when malloc() fails */
	unsigned char _ubuf[3];	/* guarantee an ungetc() buffer */
	unsigned char _nbuf[1];	/* guarantee a getc() buffer */

	/* separate buffer for fgetln() when line crosses buffer boundary */
	struct	__sbuf _lb;	/* buffer for fgetln() */

	/* Unix stdio files get aligned to block boundaries on fseek() */
	int	_blksize;	/* stat.st_blksize (may be != _bf._size) */
	fpos_t	_offset;	/* current lseek offset (see WARNING) */
"""
    _pack_ = 1
    _fields_ = [ ("_p"                 , ctypes.POINTER(ctypes.c_ubyte   ) ),
                 ("_r"                 , ctypes.c_int32                  ),
                 ("_w"                 , ctypes.c_int32                  ),
                 ("_flags"             , ctypes.c_int16                  ),
                 ("_file"              , ctypes.c_int16                  ),
                 ("Padding_160_192_"   , ctypes.c_ubyte * 4              ),
                 ("_bf"                , ctypes.c_uint128                ),
                 ("_lbfsize"           , ctypes.c_int32                  ),
                 ("Padding_352_384_"   , ctypes.c_ubyte * 4              ),
                 ("_cookie"            , ctypes.POINTER(ctypes.c_void_p  ) ),
                 ("_close"             , ctypes.POINTER(None             ) ),
                 ("_read"              , ctypes.POINTER(None             ) ),
                 ("_seek"              , ctypes.POINTER(None             ) ),
                 ("_write"             , ctypes.POINTER(None             ) ),
                 ("_ub"                , ctypes.c_uint128                ),
                 ("_extra"             , ctypes.POINTER(ctypes.c_uint128 ) ),
                 ("_ur"                , ctypes.c_int32                  ),
                 ("_ubuf"              , ctypes.c_ubyte * 3              ),
                 ("_nbuf"              , ctypes.c_ubyte * 1              ),
                 ("_lb"                , ctypes.c_uint128                ),
                 ("_blksize"           , ctypes.c_int32                  ),
                 ("Padding_1120_1152_" , ctypes.c_ubyte * 4              ),
                 ("_offset"            , ctypes.c_int64                  )]
    def SetConstants(self):
        """ Sets Constant fields to their default values """ 
        pass

librtk.satno.argtypes = [ctypes.c_int32,ctypes.c_int32]
librtk.satno.restype = ctypes.c_int32
def satno(sys,prn):
  """
satno   (int sys, int prn"""

  result = librtk.satno(sys,prn)


  return result

librtk.satsys.argtypes = [ctypes.c_int32,ctypes.POINTER(ctypes.c_int32)]
librtk.satsys.restype = ctypes.c_int32
def satsys(sat,prn):
  """
satsys  (int sat, int *prn"""

  result = librtk.satsys(sat,prn)


  return result

librtk.satid2no.argtypes = [ctypes.POINTER(ctypes.c_char)]
librtk.satid2no.restype = ctypes.c_int32
def satid2no(id):
  """
satid2no(const char *id"""

  result = librtk.satid2no(id)


  return result

librtk.satno2id.argtypes = [ctypes.c_int32,ctypes.POINTER(ctypes.c_char)]
librtk.satno2id.restype = ctypes.c_void_p
def satno2id(sat,id):
  """
satno2id(int sat, char *id"""

  result = librtk.satno2id(sat,id)


  return result

librtk.obs2code.argtypes = [ctypes.POINTER(ctypes.c_char)]
librtk.obs2code.restype = ctypes.c_ubyte
def obs2code(obs):
  """
obs2code(const char *obs"""

  result = librtk.obs2code(obs)


  return result

librtk.code2obs.argtypes = [ctypes.c_ubyte]
librtk.code2obs.restype = ctypes.POINTER(ctypes.c_char)
def code2obs(code):
  """
code2obs(uint8_t code"""

  result = librtk.code2obs(code)


  return result

librtk.code2freq.argtypes = [ctypes.c_int32,ctypes.c_ubyte,ctypes.c_int32]
librtk.code2freq.restype = ctypes.c_double
def code2freq(sys,code,fcn):
  """
code2freq(int sys, uint8_t code, int fcn"""

  result = librtk.code2freq(sys,code,fcn)


  return result

librtk.sat2freq.argtypes = [ctypes.c_int32,ctypes.c_ubyte,ctypes.POINTER(nav_t)]
librtk.sat2freq.restype = ctypes.c_double
def sat2freq(sat,code,nav):
  """
sat2freq(int sat, uint8_t code, const nav_t *nav"""

  result = librtk.sat2freq(sat,code,nav)


  return result

librtk.code2idx.argtypes = [ctypes.c_int32,ctypes.c_ubyte]
librtk.code2idx.restype = ctypes.c_int32
def code2idx(sys,code):
  """
code2idx(int sys, uint8_t code"""

  result = librtk.code2idx(sys,code)


  return result

librtk.satexclude.argtypes = [ctypes.c_int32,ctypes.c_double,ctypes.c_int32,ctypes.POINTER(prcopt_t)]
librtk.satexclude.restype = ctypes.c_int32
def satexclude(sat,var,svh,opt):
  """
satexclude(int sat, double var, int svh, const prcopt_t *opt"""

  result = librtk.satexclude(sat,var,svh,opt)


  return result

librtk.testsnr.argtypes = [ctypes.c_int32,ctypes.c_int32,ctypes.c_double,ctypes.c_double,ctypes.POINTER(snrmask_t)]
librtk.testsnr.restype = ctypes.c_int32
def testsnr(base,freq,el,snr,mask):
  """
testsnr(int base, int freq, double el, double snr,
                    const snrmask_t *mask"""

  result = librtk.testsnr(base,freq,el,snr,mask)


  return result

librtk.setcodepri.argtypes = [ctypes.c_int32,ctypes.c_int32,ctypes.POINTER(ctypes.c_char)]
librtk.setcodepri.restype = ctypes.c_void_p
def setcodepri(sys,idx,pri):
  """
setcodepri(int sys, int idx, const char *pri"""

  result = librtk.setcodepri(sys,idx,pri)


  return result

librtk.getcodepri.argtypes = [ctypes.c_int32,ctypes.c_ubyte,ctypes.POINTER(ctypes.c_char)]
librtk.getcodepri.restype = ctypes.c_int32
def getcodepri(sys,code,opt):
  """
getcodepri(int sys, uint8_t code, const char *opt"""

  result = librtk.getcodepri(sys,code,opt)


  return result

librtk.mat.argtypes = [ctypes.c_int32,ctypes.c_int32]
librtk.mat.restype = ctypes.POINTER(ctypes.c_double)
def mat(n,m):
  """
mat  (int n, int m"""

  result = librtk.mat(n,m)


  return result

librtk.imat.argtypes = [ctypes.c_int32,ctypes.c_int32]
librtk.imat.restype = ctypes.POINTER(ctypes.c_int32)
def imat(n,m):
  """
imat (int n, int m"""

  result = librtk.imat(n,m)


  return result

librtk.zeros.argtypes = [ctypes.c_int32,ctypes.c_int32]
librtk.zeros.restype = ctypes.POINTER(ctypes.c_double)
def zeros(n,m):
  """
zeros(int n, int m"""

  result = librtk.zeros(n,m)


  return result

librtk.eye.argtypes = [ctypes.c_int32]
librtk.eye.restype = ctypes.POINTER(ctypes.c_double)
def eye(n):
  """
eye  (int n"""

  result = librtk.eye(n)


  return result

librtk.dot.argtypes = [ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.c_int32]
librtk.dot.restype = ctypes.c_double
def dot(a,b,n):
  """
dot (const double *a, const double *b, int n"""

  result = librtk.dot(a,b,n)


  return result

librtk.norm.argtypes = [ctypes.POINTER(ctypes.c_double),ctypes.c_int32]
librtk.norm.restype = ctypes.c_double
def norm(a,n):
  """
norm(const double *a, int n"""

  result = librtk.norm(a,n)


  return result

librtk.cross3.argtypes = [ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
librtk.cross3.restype = ctypes.c_void_p
def cross3(a,b,c):
  """
cross3(const double *a, const double *b, double *c"""

  result = librtk.cross3(a,b,c)


  return result

librtk.normv3.argtypes = [ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
librtk.normv3.restype = ctypes.c_int32
def normv3(a,b):
  """
normv3(const double *a, double *b"""

  result = librtk.normv3(a,b)


  return result

librtk.matcpy.argtypes = [ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.c_int32,ctypes.c_int32]
librtk.matcpy.restype = ctypes.c_void_p
def matcpy(A,B,n,m):
  """
matcpy(double *A, const double *B, int n, int m"""

  result = librtk.matcpy(A,B,n,m)


  return result

librtk.matmul.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.c_int32,ctypes.c_int32,ctypes.c_int32,ctypes.c_double,ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.c_double,ctypes.POINTER(ctypes.c_double)]
librtk.matmul.restype = ctypes.c_void_p
def matmul(tr,n,k,m,alpha,A,B,beta,C):
  """
matmul(const char *tr, int n, int k, int m, double alpha,
                   const double *A, const double *B, double beta, double *C"""

  result = librtk.matmul(tr,n,k,m,alpha,A,B,beta,C)


  return result

librtk.matinv.argtypes = [ctypes.POINTER(ctypes.c_double),ctypes.c_int32]
librtk.matinv.restype = ctypes.c_int32
def matinv(A,n):
  """
matinv(double *A, int n"""

  result = librtk.matinv(A,n)


  return result

librtk.solve.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.c_int32,ctypes.c_int32,ctypes.POINTER(ctypes.c_double)]
librtk.solve.restype = ctypes.c_int32
def solve(tr,A,Y,n,m,X):
  """
solve (const char *tr, const double *A, const double *Y, int n,
                   int m, double *X"""

  result = librtk.solve(tr,A,Y,n,m,X)


  return result

librtk.lsq.argtypes = [ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.c_int32,ctypes.c_int32,ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
librtk.lsq.restype = ctypes.c_int32
def lsq(A,y,n,m,x,Q):
  """
lsq   (const double *A, const double *y, int n, int m, double *x,
                   double *Q"""

  result = librtk.lsq(A,y,n,m,x,Q)


  return result

librtk.rtkfilter.argtypes = [ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.c_int32,ctypes.c_int32]
librtk.rtkfilter.restype = ctypes.c_int32
def rtkfilter(x,P,H,v,R,n,m):
  """
rtkfilter(double *x, double *P, const double *H, const double *v,
                   const double *R, int n, int m"""

  result = librtk.rtkfilter(x,P,H,v,R,n,m)


  return result

librtk.smoother.argtypes = [ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.c_int32,ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
librtk.smoother.restype = ctypes.c_int32
def smoother(xf,Qf,xb,Qb,n,xs,Qs):
  """
smoother(const double *xf, const double *Qf, const double *xb,
                     const double *Qb, int n, double *xs, double *Qs"""

  result = librtk.smoother(xf,Qf,xb,Qb,n,xs,Qs)


  return result

librtk.matprint.argtypes = [ctypes.POINTER(ctypes.c_double),ctypes.c_int32,ctypes.c_int32,ctypes.c_int32,ctypes.c_int32]
librtk.matprint.restype = ctypes.c_void_p
def matprint(A,n,m,p,q):
  """
matprint (const double *A, int n, int m, int p, int q"""

  result = librtk.matprint(A,n,m,p,q)


  return result

librtk.matfprint.argtypes = [ctypes.POINTER(ctypes.c_double),ctypes.c_int32,ctypes.c_int32,ctypes.c_int32,ctypes.c_int32,ctypes.POINTER(__sFILE)]
librtk.matfprint.restype = ctypes.c_void_p
def matfprint(A,n,m,p,q,fp):
  """
matfprint(const double *A, int n, int m, int p, int q, FILE *fp"""

  result = librtk.matfprint(A,n,m,p,q,fp)


  return result

librtk.str2num.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.c_int32,ctypes.c_int32]
librtk.str2num.restype = ctypes.c_double
def str2num(s,i,n):
  """
str2num(const char *s, int i, int n"""

  result = librtk.str2num(s,i,n)


  return result

librtk.str2time.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.c_int32,ctypes.c_int32,ctypes.POINTER(gtime_t)]
librtk.str2time.restype = ctypes.c_int32
def str2time(s,i,n,t):
  """
str2time(const char *s, int i, int n, gtime_t *t"""

  result = librtk.str2time(s,i,n,t)


  return result

librtk.time2str.argtypes = [gtime_t,ctypes.POINTER(ctypes.c_char),ctypes.c_int32]
librtk.time2str.restype = ctypes.c_void_p
def time2str(t,str,n):
  """
time2str(gtime_t t, char *str, int n"""

  result = librtk.time2str(t,str,n)


  return result

librtk.epoch2time.argtypes = [ctypes.POINTER(ctypes.c_double)]
librtk.epoch2time.restype = gtime_t
def epoch2time(ep):
  """
epoch2time(const double *ep"""

  result = librtk.epoch2time(ep)


  return result

librtk.time2epoch.argtypes = [gtime_t,ctypes.POINTER(ctypes.c_double)]
librtk.time2epoch.restype = ctypes.c_void_p
def time2epoch(t,ep):
  """
time2epoch(gtime_t t, double *ep"""

  result = librtk.time2epoch(t,ep)


  return result

librtk.gpst2time.argtypes = [ctypes.c_int32,ctypes.c_double]
librtk.gpst2time.restype = gtime_t
def gpst2time(week,sec):
  """
gpst2time(int week, double sec"""

  result = librtk.gpst2time(week,sec)


  return result

librtk.time2gpst.argtypes = [gtime_t,ctypes.POINTER(ctypes.c_int32)]
librtk.time2gpst.restype = ctypes.c_double
def time2gpst(t,week):
  """
time2gpst(gtime_t t, int *week"""

  result = librtk.time2gpst(t,week)


  return result

librtk.gst2time.argtypes = [ctypes.c_int32,ctypes.c_double]
librtk.gst2time.restype = gtime_t
def gst2time(week,sec):
  """
gst2time(int week, double sec"""

  result = librtk.gst2time(week,sec)


  return result

librtk.time2gst.argtypes = [gtime_t,ctypes.POINTER(ctypes.c_int32)]
librtk.time2gst.restype = ctypes.c_double
def time2gst(t,week):
  """
time2gst(gtime_t t, int *week"""

  result = librtk.time2gst(t,week)


  return result

librtk.bdt2time.argtypes = [ctypes.c_int32,ctypes.c_double]
librtk.bdt2time.restype = gtime_t
def bdt2time(week,sec):
  """
bdt2time(int week, double sec"""

  result = librtk.bdt2time(week,sec)


  return result

librtk.time2bdt.argtypes = [gtime_t,ctypes.POINTER(ctypes.c_int32)]
librtk.time2bdt.restype = ctypes.c_double
def time2bdt(t,week):
  """
time2bdt(gtime_t t, int *week"""

  result = librtk.time2bdt(t,week)


  return result

librtk.time_str.argtypes = [gtime_t,ctypes.c_int32]
librtk.time_str.restype = ctypes.POINTER(ctypes.c_char)
def time_str(t,n):
  """
time_str(gtime_t t, int n"""

  result = librtk.time_str(t,n)


  return result

librtk.timeadd.argtypes = [gtime_t,ctypes.c_double]
librtk.timeadd.restype = gtime_t
def timeadd(t,sec):
  """
timeadd  (gtime_t t, double sec"""

  result = librtk.timeadd(t,sec)


  return result

librtk.timediff.argtypes = [gtime_t,gtime_t]
librtk.timediff.restype = ctypes.c_double
def timediff(t1,t2):
  """
timediff (gtime_t t1, gtime_t t2"""

  result = librtk.timediff(t1,t2)


  return result

librtk.gpst2utc.argtypes = [gtime_t]
librtk.gpst2utc.restype = gtime_t
def gpst2utc(t):
  """
gpst2utc (gtime_t t"""

  result = librtk.gpst2utc(t)


  return result

librtk.utc2gpst.argtypes = [gtime_t]
librtk.utc2gpst.restype = gtime_t
def utc2gpst(t):
  """
utc2gpst (gtime_t t"""

  result = librtk.utc2gpst(t)


  return result

librtk.gpst2bdt.argtypes = [gtime_t]
librtk.gpst2bdt.restype = gtime_t
def gpst2bdt(t):
  """
gpst2bdt (gtime_t t"""

  result = librtk.gpst2bdt(t)


  return result

librtk.bdt2gpst.argtypes = [gtime_t]
librtk.bdt2gpst.restype = gtime_t
def bdt2gpst(t):
  """
bdt2gpst (gtime_t t"""

  result = librtk.bdt2gpst(t)


  return result

librtk.timeget.argtypes = []
librtk.timeget.restype = gtime_t
def timeget():
  """
timeget  (void"""

  result = librtk.timeget()


  return result

librtk.timeset.argtypes = [gtime_t]
librtk.timeset.restype = ctypes.c_void_p
def timeset(t):
  """
timeset  (gtime_t t"""

  result = librtk.timeset(t)


  return result

librtk.timereset.argtypes = []
librtk.timereset.restype = ctypes.c_void_p
def timereset():
  """
timereset(void"""

  result = librtk.timereset()


  return result

librtk.time2doy.argtypes = [gtime_t]
librtk.time2doy.restype = ctypes.c_double
def time2doy(t):
  """
time2doy (gtime_t t"""

  result = librtk.time2doy(t)


  return result

librtk.utc2gmst.argtypes = [gtime_t,ctypes.c_double]
librtk.utc2gmst.restype = ctypes.c_double
def utc2gmst(t,ut1_utc):
  """
utc2gmst (gtime_t t, double ut1_utc"""

  result = librtk.utc2gmst(t,ut1_utc)


  return result

librtk.read_leaps.argtypes = [ctypes.POINTER(ctypes.c_char)]
librtk.read_leaps.restype = ctypes.c_int32
def read_leaps(file):
  """
read_leaps(const char *file"""

  result = librtk.read_leaps(file)


  return result

librtk.adjgpsweek.argtypes = [ctypes.c_int32]
librtk.adjgpsweek.restype = ctypes.c_int32
def adjgpsweek(week):
  """
adjgpsweek(int week"""

  result = librtk.adjgpsweek(week)


  return result

librtk.tickget.argtypes = []
librtk.tickget.restype = ctypes.c_uint32
def tickget():
  """
tickget(void"""

  result = librtk.tickget()


  return result

librtk.sleepms.argtypes = [ctypes.c_int32]
librtk.sleepms.restype = ctypes.c_void_p
def sleepms(ms):
  """
sleepms(int ms"""

  result = librtk.sleepms(ms)


  return result

librtk.reppath.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.POINTER(ctypes.c_char),gtime_t,ctypes.POINTER(ctypes.c_char),ctypes.POINTER(ctypes.c_char)]
librtk.reppath.restype = ctypes.c_int32
def reppath(path,rpath,time,rov,base):
  """
reppath(const char *path, char *rpath, gtime_t time, const char *rov,
                   const char *base"""

  result = librtk.reppath(path,rpath,time,rov,base)


  return result

librtk.ecef2pos.argtypes = [ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
librtk.ecef2pos.restype = ctypes.c_void_p
def ecef2pos(r,pos):
  """
ecef2pos(const double *r, double *pos"""

  result = librtk.ecef2pos(r,pos)


  return result

librtk.pos2ecef.argtypes = [ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
librtk.pos2ecef.restype = ctypes.c_void_p
def pos2ecef(pos,r):
  """
pos2ecef(const double *pos, double *r"""

  result = librtk.pos2ecef(pos,r)


  return result

librtk.ecef2enu.argtypes = [ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
librtk.ecef2enu.restype = ctypes.c_void_p
def ecef2enu(pos,r,e):
  """
ecef2enu(const double *pos, const double *r, double *e"""

  result = librtk.ecef2enu(pos,r,e)


  return result

librtk.enu2ecef.argtypes = [ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
librtk.enu2ecef.restype = ctypes.c_void_p
def enu2ecef(pos,e,r):
  """
enu2ecef(const double *pos, const double *e, double *r"""

  result = librtk.enu2ecef(pos,e,r)


  return result

librtk.covenu.argtypes = [ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
librtk.covenu.restype = ctypes.c_void_p
def covenu(pos,P,Q):
  """
covenu  (const double *pos, const double *P, double *Q"""

  result = librtk.covenu(pos,P,Q)


  return result

librtk.covecef.argtypes = [ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
librtk.covecef.restype = ctypes.c_void_p
def covecef(pos,Q,P):
  """
covecef (const double *pos, const double *Q, double *P"""

  result = librtk.covecef(pos,Q,P)


  return result

librtk.xyz2enu.argtypes = [ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
librtk.xyz2enu.restype = ctypes.c_void_p
def xyz2enu(pos,E):
  """
xyz2enu (const double *pos, double *E"""

  result = librtk.xyz2enu(pos,E)


  return result

librtk.eci2ecef.argtypes = [gtime_t,ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
librtk.eci2ecef.restype = ctypes.c_void_p
def eci2ecef(tutc,erpv,U,gmst):
  """
eci2ecef(gtime_t tutc, const double *erpv, double *U, double *gmst"""

  result = librtk.eci2ecef(tutc,erpv,U,gmst)


  return result

librtk.deg2dms.argtypes = [ctypes.c_double,ctypes.POINTER(ctypes.c_double),ctypes.c_int32]
librtk.deg2dms.restype = ctypes.c_void_p
def deg2dms(deg,dms,ndec):
  """
deg2dms (double deg, double *dms, int ndec"""

  result = librtk.deg2dms(deg,dms,ndec)


  return result

librtk.dms2deg.argtypes = [ctypes.POINTER(ctypes.c_double)]
librtk.dms2deg.restype = ctypes.c_double
def dms2deg(dms):
  """
dms2deg(const double *dms"""

  result = librtk.dms2deg(dms)


  return result

librtk.readpos.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.POINTER(ctypes.c_char),ctypes.POINTER(ctypes.c_double)]
librtk.readpos.restype = ctypes.c_void_p
def readpos(file,rcv,pos):
  """
readpos(const char *file, const char *rcv, double *pos"""

  result = librtk.readpos(file,rcv,pos)


  return result

librtk.sortobs.argtypes = [ctypes.POINTER(obs_t)]
librtk.sortobs.restype = ctypes.c_int32
def sortobs(obs):
  """
sortobs(obs_t *obs"""

  result = librtk.sortobs(obs)


  return result

librtk.uniqnav.argtypes = [ctypes.POINTER(nav_t)]
librtk.uniqnav.restype = ctypes.c_void_p
def uniqnav(nav):
  """
uniqnav(nav_t *nav"""

  result = librtk.uniqnav(nav)


  return result

librtk.screent.argtypes = [gtime_t,gtime_t,gtime_t,ctypes.c_double]
librtk.screent.restype = ctypes.c_int32
def screent(time,ts,te,tint):
  """
screent(gtime_t time, gtime_t ts, gtime_t te, double tint"""

  result = librtk.screent(time,ts,te,tint)


  return result

librtk.readnav.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.POINTER(nav_t)]
librtk.readnav.restype = ctypes.c_int32
def readnav(file,nav):
  """
readnav(const char *file, nav_t *nav"""

  result = librtk.readnav(file,nav)


  return result

librtk.savenav.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.POINTER(nav_t)]
librtk.savenav.restype = ctypes.c_int32
def savenav(file,nav):
  """
savenav(const char *file, const nav_t *nav"""

  result = librtk.savenav(file,nav)


  return result

librtk.freeobs.argtypes = [ctypes.POINTER(obs_t)]
librtk.freeobs.restype = ctypes.c_void_p
def freeobs(obs):
  """
freeobs(obs_t *obs"""

  result = librtk.freeobs(obs)


  return result

librtk.freenav.argtypes = [ctypes.POINTER(nav_t),ctypes.c_int32]
librtk.freenav.restype = ctypes.c_void_p
def freenav(nav,opt):
  """
freenav(nav_t *nav, int opt"""

  result = librtk.freenav(nav,opt)


  return result

librtk.readblq.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.POINTER(ctypes.c_char),ctypes.POINTER(ctypes.c_double)]
librtk.readblq.restype = ctypes.c_int32
def readblq(file,sta,odisp):
  """
readblq(const char *file, const char *sta, double *odisp"""

  result = librtk.readblq(file,sta,odisp)


  return result

librtk.readerp.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.POINTER(erp_t)]
librtk.readerp.restype = ctypes.c_int32
def readerp(file,erp):
  """
readerp(const char *file, erp_t *erp"""

  result = librtk.readerp(file,erp)


  return result

librtk.geterp.argtypes = [ctypes.POINTER(erp_t),gtime_t,ctypes.POINTER(ctypes.c_double)]
librtk.geterp.restype = ctypes.c_int32
def geterp(erp,time,val):
  """
geterp (const erp_t *erp, gtime_t time, double *val"""

  result = librtk.geterp(erp,time,val)


  return result

librtk.rtktraceopen.argtypes = [ctypes.POINTER(ctypes.c_char)]
librtk.rtktraceopen.restype = ctypes.c_void_p
def rtktraceopen(file):
  """
rtktraceopen(const char *file"""

  result = librtk.rtktraceopen(file)


  return result

librtk.rtktraceclose.argtypes = []
librtk.rtktraceclose.restype = ctypes.c_void_p
def rtktraceclose():
  """
rtktraceclose(void"""

  result = librtk.rtktraceclose()


  return result

librtk.rtktracelevel.argtypes = [ctypes.c_int32]
librtk.rtktracelevel.restype = ctypes.c_void_p
def rtktracelevel(level):
  """
rtktracelevel(int level"""

  result = librtk.rtktracelevel(level)


  return result

librtk.rtktrace.argtypes = [ctypes.c_int32,ctypes.POINTER(ctypes.c_char)]
librtk.rtktrace.restype = ctypes.c_void_p
def rtktrace(level,format):
  """
rtktrace    (int level, const char *format, ..."""

  result = librtk.rtktrace(level,format)


  return result

librtk.rtktracet.argtypes = [ctypes.c_int32,ctypes.POINTER(ctypes.c_char)]
librtk.rtktracet.restype = ctypes.c_void_p
def rtktracet(level,format):
  """
rtktracet   (int level, const char *format, ..."""

  result = librtk.rtktracet(level,format)


  return result

librtk.rtktracemat.argtypes = [ctypes.c_int32,ctypes.POINTER(ctypes.c_double),ctypes.c_int32,ctypes.c_int32,ctypes.c_int32,ctypes.c_int32]
librtk.rtktracemat.restype = ctypes.c_void_p
def rtktracemat(level,A,n,m,p,q):
  """
rtktracemat (int level, const double *A, int n, int m, int p, int q"""

  result = librtk.rtktracemat(level,A,n,m,p,q)


  return result

librtk.rtktraceobs.argtypes = [ctypes.c_int32,ctypes.POINTER(obsd_t),ctypes.c_int32]
librtk.rtktraceobs.restype = ctypes.c_void_p
def rtktraceobs(level,obs,n):
  """
rtktraceobs (int level, const obsd_t *obs, int n"""

  result = librtk.rtktraceobs(level,obs,n)


  return result

librtk.rtktracenav.argtypes = [ctypes.c_int32,ctypes.POINTER(nav_t)]
librtk.rtktracenav.restype = ctypes.c_void_p
def rtktracenav(level,nav):
  """
rtktracenav (int level, const nav_t *nav"""

  result = librtk.rtktracenav(level,nav)


  return result

librtk.rtktracegnav.argtypes = [ctypes.c_int32,ctypes.POINTER(nav_t)]
librtk.rtktracegnav.restype = ctypes.c_void_p
def rtktracegnav(level,nav):
  """
rtktracegnav(int level, const nav_t *nav"""

  result = librtk.rtktracegnav(level,nav)


  return result

librtk.rtktracehnav.argtypes = [ctypes.c_int32,ctypes.POINTER(nav_t)]
librtk.rtktracehnav.restype = ctypes.c_void_p
def rtktracehnav(level,nav):
  """
rtktracehnav(int level, const nav_t *nav"""

  result = librtk.rtktracehnav(level,nav)


  return result

librtk.rtktracepeph.argtypes = [ctypes.c_int32,ctypes.POINTER(nav_t)]
librtk.rtktracepeph.restype = ctypes.c_void_p
def rtktracepeph(level,nav):
  """
rtktracepeph(int level, const nav_t *nav"""

  result = librtk.rtktracepeph(level,nav)


  return result

librtk.rtktracepclk.argtypes = [ctypes.c_int32,ctypes.POINTER(nav_t)]
librtk.rtktracepclk.restype = ctypes.c_void_p
def rtktracepclk(level,nav):
  """
rtktracepclk(int level, const nav_t *nav"""

  result = librtk.rtktracepclk(level,nav)


  return result

librtk.rtktraceb.argtypes = [ctypes.c_int32,ctypes.POINTER(ctypes.c_ubyte),ctypes.c_int32]
librtk.rtktraceb.restype = ctypes.c_void_p
def rtktraceb(level,p,n):
  """
rtktraceb   (int level, const uint8_t *p, int n"""

  result = librtk.rtktraceb(level,p,n)


  return result

librtk.execcmd.argtypes = [ctypes.POINTER(ctypes.c_char)]
librtk.execcmd.restype = ctypes.c_int32
def execcmd(cmd):
  """
execcmd(const char *cmd"""

  result = librtk.execcmd(cmd)


  return result

librtk.createdir.argtypes = [ctypes.POINTER(ctypes.c_char)]
librtk.createdir.restype = ctypes.c_void_p
def createdir(path):
  """
createdir(const char *path"""

  result = librtk.createdir(path)


  return result

librtk.satazel.argtypes = [ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
librtk.satazel.restype = ctypes.c_double
def satazel(pos,e,azel):
  """
satazel(const double *pos, const double *e, double *azel"""

  result = librtk.satazel(pos,e,azel)


  return result

librtk.geodist.argtypes = [ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
librtk.geodist.restype = ctypes.c_double
def geodist(rs,rr,e):
  """
geodist(const double *rs, const double *rr, double *e"""

  result = librtk.geodist(rs,rr,e)


  return result

librtk.dops.argtypes = [ctypes.c_int32,ctypes.POINTER(ctypes.c_double),ctypes.c_double,ctypes.POINTER(ctypes.c_double)]
librtk.dops.restype = ctypes.c_void_p
def dops(ns,azel,elmin,dop):
  """
dops(int ns, const double *azel, double elmin, double *dop"""

  result = librtk.dops(ns,azel,elmin,dop)


  return result

librtk.ionmodel.argtypes = [gtime_t,ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
librtk.ionmodel.restype = ctypes.c_double
def ionmodel(t,ion,pos,azel):
  """
ionmodel(gtime_t t, const double *ion, const double *pos,
                       const double *azel"""

  result = librtk.ionmodel(t,ion,pos,azel)


  return result

librtk.ionmapf.argtypes = [ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
librtk.ionmapf.restype = ctypes.c_double
def ionmapf(pos,azel):
  """
ionmapf(const double *pos, const double *azel"""

  result = librtk.ionmapf(pos,azel)


  return result

librtk.ionppp.argtypes = [ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.c_double,ctypes.c_double,ctypes.POINTER(ctypes.c_double)]
librtk.ionppp.restype = ctypes.c_double
def ionppp(pos,azel,re,hion,pppos):
  """
ionppp(const double *pos, const double *azel, double re,
                     double hion, double *pppos"""

  result = librtk.ionppp(pos,azel,re,hion,pppos)


  return result

librtk.tropmodel.argtypes = [gtime_t,ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.c_double]
librtk.tropmodel.restype = ctypes.c_double
def tropmodel(time,pos,azel,humi):
  """
tropmodel(gtime_t time, const double *pos, const double *azel,
                        double humi"""

  result = librtk.tropmodel(time,pos,azel,humi)


  return result

librtk.tropmapf.argtypes = [gtime_t,ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
librtk.tropmapf.restype = ctypes.c_double
def tropmapf(time,pos,azel,mapfw):
  """
tropmapf(gtime_t time, const double *pos, const double *azel,
                       double *mapfw"""

  result = librtk.tropmapf(time,pos,azel,mapfw)


  return result

librtk.iontec.argtypes = [gtime_t,ctypes.POINTER(nav_t),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.c_int32,ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
librtk.iontec.restype = ctypes.c_int32
def iontec(time,nav,pos,azel,opt,delay,var):
  """
iontec(gtime_t time, const nav_t *nav, const double *pos,
                  const double *azel, int opt, double *delay, double *var"""

  result = librtk.iontec(time,nav,pos,azel,opt,delay,var)


  return result

librtk.readtec.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.POINTER(nav_t),ctypes.c_int32]
librtk.readtec.restype = ctypes.c_void_p
def readtec(file,nav,opt):
  """
readtec(const char *file, nav_t *nav, int opt"""

  result = librtk.readtec(file,nav,opt)


  return result

librtk.ionocorr.argtypes = [gtime_t,ctypes.POINTER(nav_t),ctypes.c_int32,ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.c_int32,ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
librtk.ionocorr.restype = ctypes.c_int32
def ionocorr(time,nav,sat,pos,azel,ionoopt,ion,var):
  """
ionocorr(gtime_t time, const nav_t *nav, int sat, const double *pos,
                    const double *azel, int ionoopt, double *ion, double *var"""

  result = librtk.ionocorr(time,nav,sat,pos,azel,ionoopt,ion,var)


  return result

librtk.tropcorr.argtypes = [gtime_t,ctypes.POINTER(nav_t),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.c_int32,ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
librtk.tropcorr.restype = ctypes.c_int32
def tropcorr(time,nav,pos,azel,tropopt,trp,var):
  """
tropcorr(gtime_t time, const nav_t *nav, const double *pos,
                    const double *azel, int tropopt, double *trp, double *var"""

  result = librtk.tropcorr(time,nav,pos,azel,tropopt,trp,var)


  return result

librtk.readpcv.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.POINTER(pcvs_t)]
librtk.readpcv.restype = ctypes.c_int32
def readpcv(file,pcvs):
  """
readpcv(const char *file, pcvs_t *pcvs"""

  result = librtk.readpcv(file,pcvs)


  return result

librtk.antmodel.argtypes = [ctypes.POINTER(pcv_t),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.c_int32,ctypes.POINTER(ctypes.c_double)]
librtk.antmodel.restype = ctypes.c_void_p
def antmodel(pcv,del_,azel,opt,dant):
  """
antmodel(const pcv_t *pcv, const double *del, const double *azel,
                     int opt, double *dant"""

  result = librtk.antmodel(pcv,del_,azel,opt,dant)


  return result

librtk.antmodel_s.argtypes = [ctypes.POINTER(pcv_t),ctypes.c_double,ctypes.POINTER(ctypes.c_double)]
librtk.antmodel_s.restype = ctypes.c_void_p
def antmodel_s(pcv,nadir,dant):
  """
antmodel_s(const pcv_t *pcv, double nadir, double *dant"""

  result = librtk.antmodel_s(pcv,nadir,dant)


  return result

librtk.sunmoonpos.argtypes = [gtime_t,ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
librtk.sunmoonpos.restype = ctypes.c_void_p
def sunmoonpos(tutc,erpv,rsun,rmoon,gmst):
  """
sunmoonpos(gtime_t tutc, const double *erpv, double *rsun,
                       double *rmoon, double *gmst"""

  result = librtk.sunmoonpos(tutc,erpv,rsun,rmoon,gmst)


  return result

librtk.tidedisp.argtypes = [gtime_t,ctypes.POINTER(ctypes.c_double),ctypes.c_int32,ctypes.POINTER(erp_t),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
librtk.tidedisp.restype = ctypes.c_void_p
def tidedisp(tutc,rr,opt,erp,odisp,dr):
  """
tidedisp(gtime_t tutc, const double *rr, int opt, const erp_t *erp,
                     const double *odisp, double *dr"""

  result = librtk.tidedisp(tutc,rr,opt,erp,odisp,dr)


  return result

librtk.opengeoid.argtypes = [ctypes.c_int32,ctypes.POINTER(ctypes.c_char)]
librtk.opengeoid.restype = ctypes.c_int32
def opengeoid(model,file):
  """
opengeoid(int model, const char *file"""

  result = librtk.opengeoid(model,file)


  return result

librtk.closegeoid.argtypes = []
librtk.closegeoid.restype = ctypes.c_void_p
def closegeoid():
  """
closegeoid(void"""

  result = librtk.closegeoid()


  return result

librtk.geoidh.argtypes = [ctypes.POINTER(ctypes.c_double)]
librtk.geoidh.restype = ctypes.c_double
def geoidh(pos):
  """
geoidh(const double *pos"""

  result = librtk.geoidh(pos)


  return result

librtk.loaddatump.argtypes = [ctypes.POINTER(ctypes.c_char)]
librtk.loaddatump.restype = ctypes.c_int32
def loaddatump(file):
  """
loaddatump(const char *file"""

  result = librtk.loaddatump(file)


  return result

librtk.tokyo2jgd.argtypes = [ctypes.POINTER(ctypes.c_double)]
librtk.tokyo2jgd.restype = ctypes.c_int32
def tokyo2jgd(pos):
  """
tokyo2jgd(double *pos"""

  result = librtk.tokyo2jgd(pos)


  return result

librtk.jgd2tokyo.argtypes = [ctypes.POINTER(ctypes.c_double)]
librtk.jgd2tokyo.restype = ctypes.c_int32
def jgd2tokyo(pos):
  """
jgd2tokyo(double *pos"""

  result = librtk.jgd2tokyo(pos)


  return result

librtk.readrnx.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.c_int32,ctypes.POINTER(ctypes.c_char),ctypes.POINTER(obs_t),ctypes.POINTER(nav_t),ctypes.POINTER(sta_t)]
librtk.readrnx.restype = ctypes.c_int32
def readrnx(file,rcv,opt,obs,nav,sta):
  """
readrnx (const char *file, int rcv, const char *opt, obs_t *obs,
                    nav_t *nav, sta_t *sta"""

  result = librtk.readrnx(file,rcv,opt,obs,nav,sta)


  return result

librtk.readrnxt.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.c_int32,gtime_t,gtime_t,ctypes.c_double,ctypes.POINTER(ctypes.c_char),ctypes.POINTER(obs_t),ctypes.POINTER(nav_t),ctypes.POINTER(sta_t)]
librtk.readrnxt.restype = ctypes.c_int32
def readrnxt(file,rcv,ts,te,tint,opt,obs,nav,sta):
  """
readrnxt(const char *file, int rcv, gtime_t ts, gtime_t te,
                    double tint, const char *opt, obs_t *obs, nav_t *nav,
                    sta_t *sta"""

  result = librtk.readrnxt(file,rcv,ts,te,tint,opt,obs,nav,sta)


  return result

librtk.readrnxc.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.POINTER(nav_t)]
librtk.readrnxc.restype = ctypes.c_int32
def readrnxc(file,nav):
  """
readrnxc(const char *file, nav_t *nav"""

  result = librtk.readrnxc(file,nav)


  return result

librtk.outrnxobsh.argtypes = [ctypes.POINTER(__sFILE),ctypes.POINTER(rnxopt_t),ctypes.POINTER(nav_t)]
librtk.outrnxobsh.restype = ctypes.c_int32
def outrnxobsh(fp,opt,nav):
  """
outrnxobsh(FILE *fp, const rnxopt_t *opt, const nav_t *nav"""

  result = librtk.outrnxobsh(fp,opt,nav)


  return result

librtk.outrnxobsb.argtypes = [ctypes.POINTER(__sFILE),ctypes.POINTER(rnxopt_t),ctypes.POINTER(obsd_t),ctypes.c_int32,ctypes.c_int32]
librtk.outrnxobsb.restype = ctypes.c_int32
def outrnxobsb(fp,opt,obs,n,epflag):
  """
outrnxobsb(FILE *fp, const rnxopt_t *opt, const obsd_t *obs, int n,
                      int epflag"""

  result = librtk.outrnxobsb(fp,opt,obs,n,epflag)


  return result

librtk.outrnxnavh.argtypes = [ctypes.POINTER(__sFILE),ctypes.POINTER(rnxopt_t),ctypes.POINTER(nav_t)]
librtk.outrnxnavh.restype = ctypes.c_int32
def outrnxnavh(fp,opt,nav):
  """
outrnxnavh (FILE *fp, const rnxopt_t *opt, const nav_t *nav"""

  result = librtk.outrnxnavh(fp,opt,nav)


  return result

librtk.outrnxgnavh.argtypes = [ctypes.POINTER(__sFILE),ctypes.POINTER(rnxopt_t),ctypes.POINTER(nav_t)]
librtk.outrnxgnavh.restype = ctypes.c_int32
def outrnxgnavh(fp,opt,nav):
  """
outrnxgnavh(FILE *fp, const rnxopt_t *opt, const nav_t *nav"""

  result = librtk.outrnxgnavh(fp,opt,nav)


  return result

librtk.outrnxhnavh.argtypes = [ctypes.POINTER(__sFILE),ctypes.POINTER(rnxopt_t),ctypes.POINTER(nav_t)]
librtk.outrnxhnavh.restype = ctypes.c_int32
def outrnxhnavh(fp,opt,nav):
  """
outrnxhnavh(FILE *fp, const rnxopt_t *opt, const nav_t *nav"""

  result = librtk.outrnxhnavh(fp,opt,nav)


  return result

librtk.outrnxlnavh.argtypes = [ctypes.POINTER(__sFILE),ctypes.POINTER(rnxopt_t),ctypes.POINTER(nav_t)]
librtk.outrnxlnavh.restype = ctypes.c_int32
def outrnxlnavh(fp,opt,nav):
  """
outrnxlnavh(FILE *fp, const rnxopt_t *opt, const nav_t *nav"""

  result = librtk.outrnxlnavh(fp,opt,nav)


  return result

librtk.outrnxqnavh.argtypes = [ctypes.POINTER(__sFILE),ctypes.POINTER(rnxopt_t),ctypes.POINTER(nav_t)]
librtk.outrnxqnavh.restype = ctypes.c_int32
def outrnxqnavh(fp,opt,nav):
  """
outrnxqnavh(FILE *fp, const rnxopt_t *opt, const nav_t *nav"""

  result = librtk.outrnxqnavh(fp,opt,nav)


  return result

librtk.outrnxcnavh.argtypes = [ctypes.POINTER(__sFILE),ctypes.POINTER(rnxopt_t),ctypes.POINTER(nav_t)]
librtk.outrnxcnavh.restype = ctypes.c_int32
def outrnxcnavh(fp,opt,nav):
  """
outrnxcnavh(FILE *fp, const rnxopt_t *opt, const nav_t *nav"""

  result = librtk.outrnxcnavh(fp,opt,nav)


  return result

librtk.outrnxinavh.argtypes = [ctypes.POINTER(__sFILE),ctypes.POINTER(rnxopt_t),ctypes.POINTER(nav_t)]
librtk.outrnxinavh.restype = ctypes.c_int32
def outrnxinavh(fp,opt,nav):
  """
outrnxinavh(FILE *fp, const rnxopt_t *opt, const nav_t *nav"""

  result = librtk.outrnxinavh(fp,opt,nav)


  return result

librtk.outrnxnavb.argtypes = [ctypes.POINTER(__sFILE),ctypes.POINTER(rnxopt_t),ctypes.POINTER(eph_t)]
librtk.outrnxnavb.restype = ctypes.c_int32
def outrnxnavb(fp,opt,eph):
  """
outrnxnavb (FILE *fp, const rnxopt_t *opt, const eph_t *eph"""

  result = librtk.outrnxnavb(fp,opt,eph)


  return result

librtk.outrnxgnavb.argtypes = [ctypes.POINTER(__sFILE),ctypes.POINTER(rnxopt_t),ctypes.POINTER(geph_t)]
librtk.outrnxgnavb.restype = ctypes.c_int32
def outrnxgnavb(fp,opt,geph):
  """
outrnxgnavb(FILE *fp, const rnxopt_t *opt, const geph_t *geph"""

  result = librtk.outrnxgnavb(fp,opt,geph)


  return result

librtk.outrnxhnavb.argtypes = [ctypes.POINTER(__sFILE),ctypes.POINTER(rnxopt_t),ctypes.POINTER(seph_t)]
librtk.outrnxhnavb.restype = ctypes.c_int32
def outrnxhnavb(fp,opt,seph):
  """
outrnxhnavb(FILE *fp, const rnxopt_t *opt, const seph_t *seph"""

  result = librtk.outrnxhnavb(fp,opt,seph)


  return result

librtk.rtk_uncompress.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.POINTER(ctypes.c_char)]
librtk.rtk_uncompress.restype = ctypes.c_int32
def rtk_uncompress(file,uncfile):
  """
rtk_uncompress(const char *file, char *uncfile"""

  result = librtk.rtk_uncompress(file,uncfile)


  return result

librtk.convrnx.argtypes = [ctypes.c_int32,ctypes.POINTER(rnxopt_t),ctypes.POINTER(ctypes.c_char),ctypes.POINTER(ctypes.c_char)]
librtk.convrnx.restype = ctypes.c_int32
def convrnx(format,opt,file,ofile):
  """
convrnx(int format, rnxopt_t *opt, const char *file, char **ofile"""

  result = librtk.convrnx(format,opt,file,ofile)


  return result

librtk.init_rnxctr.argtypes = [ctypes.POINTER(rnxctr_t)]
librtk.init_rnxctr.restype = ctypes.c_int32
def init_rnxctr(rnx):
  """
init_rnxctr (rnxctr_t *rnx"""

  result = librtk.init_rnxctr(rnx)


  return result

librtk.free_rnxctr.argtypes = [ctypes.POINTER(rnxctr_t)]
librtk.free_rnxctr.restype = ctypes.c_void_p
def free_rnxctr(rnx):
  """
free_rnxctr (rnxctr_t *rnx"""

  result = librtk.free_rnxctr(rnx)


  return result

librtk.open_rnxctr.argtypes = [ctypes.POINTER(rnxctr_t),ctypes.POINTER(__sFILE)]
librtk.open_rnxctr.restype = ctypes.c_int32
def open_rnxctr(rnx,fp):
  """
open_rnxctr (rnxctr_t *rnx, FILE *fp"""

  result = librtk.open_rnxctr(rnx,fp)


  return result

librtk.input_rnxctr.argtypes = [ctypes.POINTER(rnxctr_t),ctypes.POINTER(__sFILE)]
librtk.input_rnxctr.restype = ctypes.c_int32
def input_rnxctr(rnx,fp):
  """
input_rnxctr(rnxctr_t *rnx, FILE *fp"""

  result = librtk.input_rnxctr(rnx,fp)


  return result

librtk.seleph.argtypes = [gtime_t,ctypes.c_int32,ctypes.c_int32,ctypes.POINTER(nav_t)]
librtk.seleph.restype = ctypes.POINTER(eph_t)
def seleph(time,sat,iode,nav):
  """
seleph(gtime_t time, int sat, int iode, const nav_t *nav"""

  result = librtk.seleph(time,sat,iode,nav)


  return result

librtk.eph2clk.argtypes = [gtime_t,ctypes.POINTER(eph_t)]
librtk.eph2clk.restype = ctypes.c_double
def eph2clk(time,eph):
  """
eph2clk (gtime_t time, const eph_t  *eph"""

  result = librtk.eph2clk(time,eph)


  return result

librtk.geph2clk.argtypes = [gtime_t,ctypes.POINTER(geph_t)]
librtk.geph2clk.restype = ctypes.c_double
def geph2clk(time,geph):
  """
geph2clk(gtime_t time, const geph_t *geph"""

  result = librtk.geph2clk(time,geph)


  return result

librtk.seph2clk.argtypes = [gtime_t,ctypes.POINTER(seph_t)]
librtk.seph2clk.restype = ctypes.c_double
def seph2clk(time,seph):
  """
seph2clk(gtime_t time, const seph_t *seph"""

  result = librtk.seph2clk(time,seph)


  return result

librtk.eph2pos.argtypes = [gtime_t,ctypes.POINTER(eph_t),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
librtk.eph2pos.restype = ctypes.c_void_p
def eph2pos(time,eph,rs,dts,var):
  """
eph2pos (gtime_t time, const eph_t  *eph,  double *rs, double *dts,
                     double *var"""

  result = librtk.eph2pos(time,eph,rs,dts,var)


  return result

librtk.geph2pos.argtypes = [gtime_t,ctypes.POINTER(geph_t),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
librtk.geph2pos.restype = ctypes.c_void_p
def geph2pos(time,geph,rs,dts,var):
  """
geph2pos(gtime_t time, const geph_t *geph, double *rs, double *dts,
                     double *var"""

  result = librtk.geph2pos(time,geph,rs,dts,var)


  return result

librtk.seph2pos.argtypes = [gtime_t,ctypes.POINTER(seph_t),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
librtk.seph2pos.restype = ctypes.c_void_p
def seph2pos(time,seph,rs,dts,var):
  """
seph2pos(gtime_t time, const seph_t *seph, double *rs, double *dts,
                     double *var"""

  result = librtk.seph2pos(time,seph,rs,dts,var)


  return result

librtk.peph2pos.argtypes = [gtime_t,ctypes.c_int32,ctypes.POINTER(nav_t),ctypes.c_int32,ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
librtk.peph2pos.restype = ctypes.c_int32
def peph2pos(time,sat,nav,opt,rs,dts,var):
  """
peph2pos(gtime_t time, int sat, const nav_t *nav, int opt,
                     double *rs, double *dts, double *var"""

  result = librtk.peph2pos(time,sat,nav,opt,rs,dts,var)


  return result

librtk.satantoff.argtypes = [gtime_t,ctypes.POINTER(ctypes.c_double),ctypes.c_int32,ctypes.POINTER(nav_t),ctypes.POINTER(ctypes.c_double)]
librtk.satantoff.restype = ctypes.c_void_p
def satantoff(time,rs,sat,nav,dant):
  """
satantoff(gtime_t time, const double *rs, int sat, const nav_t *nav,
                      double *dant"""

  result = librtk.satantoff(time,rs,sat,nav,dant)


  return result

librtk.satpos.argtypes = [gtime_t,gtime_t,ctypes.c_int32,ctypes.c_int32,ctypes.POINTER(nav_t),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_int32)]
librtk.satpos.restype = ctypes.c_int32
def satpos(time,teph,sat,ephopt,nav,rs,dts,var,svh):
  """
satpos(gtime_t time, gtime_t teph, int sat, int ephopt,
                   const nav_t *nav, double *rs, double *dts, double *var,
                   int *svh"""

  result = librtk.satpos(time,teph,sat,ephopt,nav,rs,dts,var,svh)


  return result

librtk.satposs.argtypes = [gtime_t,ctypes.POINTER(obsd_t),ctypes.c_int32,ctypes.POINTER(nav_t),ctypes.c_int32,ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_int32)]
librtk.satposs.restype = ctypes.c_void_p
def satposs(time,obs,n,nav,sateph,rs,dts,var,svh):
  """
satposs(gtime_t time, const obsd_t *obs, int n, const nav_t *nav,
                    int sateph, double *rs, double *dts, double *var, int *svh"""

  result = librtk.satposs(time,obs,n,nav,sateph,rs,dts,var,svh)


  return result

librtk.setseleph.argtypes = [ctypes.c_int32,ctypes.c_int32]
librtk.setseleph.restype = ctypes.c_void_p
def setseleph(sys,sel):
  """
setseleph(int sys, int sel"""

  result = librtk.setseleph(sys,sel)


  return result

librtk.getseleph.argtypes = [ctypes.c_int32]
librtk.getseleph.restype = ctypes.c_int32
def getseleph(sys):
  """
getseleph(int sys"""

  result = librtk.getseleph(sys)


  return result

librtk.readsp3.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.POINTER(nav_t),ctypes.c_int32]
librtk.readsp3.restype = ctypes.c_void_p
def readsp3(file,nav,opt):
  """
readsp3(const char *file, nav_t *nav, int opt"""

  result = librtk.readsp3(file,nav,opt)


  return result

librtk.readsap.argtypes = [ctypes.POINTER(ctypes.c_char),gtime_t,ctypes.POINTER(nav_t)]
librtk.readsap.restype = ctypes.c_int32
def readsap(file,time,nav):
  """
readsap(const char *file, gtime_t time, nav_t *nav"""

  result = librtk.readsap(file,time,nav)


  return result

librtk.readdcb.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.POINTER(nav_t),ctypes.POINTER(sta_t)]
librtk.readdcb.restype = ctypes.c_int32
def readdcb(file,nav,sta):
  """
readdcb(const char *file, nav_t *nav, const sta_t *sta"""

  result = librtk.readdcb(file,nav,sta)


  return result

librtk.alm2pos.argtypes = [gtime_t,ctypes.POINTER(alm_t),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
librtk.alm2pos.restype = ctypes.c_void_p
def alm2pos(time,alm,rs,dts):
  """
alm2pos(gtime_t time, const alm_t *alm, double *rs, double *dts"""

  result = librtk.alm2pos(time,alm,rs,dts)


  return result

librtk.tle_read.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.POINTER(tle_t)]
librtk.tle_read.restype = ctypes.c_int32
def tle_read(file,tle):
  """
tle_read(const char *file, tle_t *tle"""

  result = librtk.tle_read(file,tle)


  return result

librtk.tle_name_read.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.POINTER(tle_t)]
librtk.tle_name_read.restype = ctypes.c_int32
def tle_name_read(file,tle):
  """
tle_name_read(const char *file, tle_t *tle"""

  result = librtk.tle_name_read(file,tle)


  return result

librtk.tle_pos.argtypes = [gtime_t,ctypes.POINTER(ctypes.c_char),ctypes.POINTER(ctypes.c_char),ctypes.POINTER(ctypes.c_char),ctypes.POINTER(tle_t),ctypes.POINTER(erp_t),ctypes.POINTER(ctypes.c_double)]
librtk.tle_pos.restype = ctypes.c_int32
def tle_pos(time,name,satno,desig,tle,erp,rs):
  """
tle_pos(gtime_t time, const char *name, const char *satno,
                   const char *desig, const tle_t *tle, const erp_t *erp,
                   double *rs"""

  result = librtk.tle_pos(time,name,satno,desig,tle,erp,rs)


  return result

librtk.getbitu.argtypes = [ctypes.POINTER(ctypes.c_ubyte),ctypes.c_int32,ctypes.c_int32]
librtk.getbitu.restype = ctypes.c_uint32
def getbitu(buff,pos,len):
  """
getbitu(const uint8_t *buff, int pos, int len"""

  result = librtk.getbitu(buff,pos,len)


  return result

librtk.getbits.argtypes = [ctypes.POINTER(ctypes.c_ubyte),ctypes.c_int32,ctypes.c_int32]
librtk.getbits.restype = ctypes.c_int32
def getbits(buff,pos,len):
  """
getbits(const uint8_t *buff, int pos, int len"""

  result = librtk.getbits(buff,pos,len)


  return result

librtk.setbitu.argtypes = [ctypes.POINTER(ctypes.c_ubyte),ctypes.c_int32,ctypes.c_int32,ctypes.c_uint32]
librtk.setbitu.restype = ctypes.c_void_p
def setbitu(buff,pos,len,data):
  """
setbitu(uint8_t *buff, int pos, int len, uint32_t data"""

  result = librtk.setbitu(buff,pos,len,data)


  return result

librtk.setbits.argtypes = [ctypes.POINTER(ctypes.c_ubyte),ctypes.c_int32,ctypes.c_int32,ctypes.c_int32]
librtk.setbits.restype = ctypes.c_void_p
def setbits(buff,pos,len,data):
  """
setbits(uint8_t *buff, int pos, int len, int32_t  data"""

  result = librtk.setbits(buff,pos,len,data)


  return result

librtk.rtk_crc32.argtypes = [ctypes.POINTER(ctypes.c_ubyte),ctypes.c_int32]
librtk.rtk_crc32.restype = ctypes.c_uint32
def rtk_crc32(buff,len):
  """
rtk_crc32 (const uint8_t *buff, int len"""

  result = librtk.rtk_crc32(buff,len)


  return result

librtk.rtk_crc24q.argtypes = [ctypes.POINTER(ctypes.c_ubyte),ctypes.c_int32]
librtk.rtk_crc24q.restype = ctypes.c_uint32
def rtk_crc24q(buff,len):
  """
rtk_crc24q(const uint8_t *buff, int len"""

  result = librtk.rtk_crc24q(buff,len)


  return result

librtk.rtk_crc16.argtypes = [ctypes.POINTER(ctypes.c_ubyte),ctypes.c_int32]
librtk.rtk_crc16.restype = ctypes.c_uint16
def rtk_crc16(buff,len):
  """
rtk_crc16 (const uint8_t *buff, int len"""

  result = librtk.rtk_crc16(buff,len)


  return result

librtk.decode_word.argtypes = [ctypes.c_uint32,ctypes.POINTER(ctypes.c_ubyte)]
librtk.decode_word.restype = ctypes.c_int32
def decode_word(word,data):
  """
decode_word (uint32_t word, uint8_t *data"""

  result = librtk.decode_word(word,data)


  return result

librtk.decode_frame.argtypes = [ctypes.POINTER(ctypes.c_ubyte),ctypes.POINTER(eph_t),ctypes.POINTER(alm_t),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
librtk.decode_frame.restype = ctypes.c_int32
def decode_frame(buff,eph,alm,ion,utc):
  """
decode_frame(const uint8_t *buff, eph_t *eph, alm_t *alm,
                        double *ion, double *utc"""

  result = librtk.decode_frame(buff,eph,alm,ion,utc)


  return result

librtk.test_glostr.argtypes = [ctypes.POINTER(ctypes.c_ubyte)]
librtk.test_glostr.restype = ctypes.c_int32
def test_glostr(buff):
  """
test_glostr(const uint8_t *buff"""

  result = librtk.test_glostr(buff)


  return result

librtk.decode_glostr.argtypes = [ctypes.POINTER(ctypes.c_ubyte),ctypes.POINTER(geph_t),ctypes.POINTER(ctypes.c_double)]
librtk.decode_glostr.restype = ctypes.c_int32
def decode_glostr(buff,geph,utc):
  """
decode_glostr(const uint8_t *buff, geph_t *geph, double *utc"""

  result = librtk.decode_glostr(buff,geph,utc)


  return result

librtk.decode_bds_d1.argtypes = [ctypes.POINTER(ctypes.c_ubyte),ctypes.POINTER(eph_t),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
librtk.decode_bds_d1.restype = ctypes.c_int32
def decode_bds_d1(buff,eph,ion,utc):
  """
decode_bds_d1(const uint8_t *buff, eph_t *eph, double *ion,
                         double *utc"""

  result = librtk.decode_bds_d1(buff,eph,ion,utc)


  return result

librtk.decode_bds_d2.argtypes = [ctypes.POINTER(ctypes.c_ubyte),ctypes.POINTER(eph_t),ctypes.POINTER(ctypes.c_double)]
librtk.decode_bds_d2.restype = ctypes.c_int32
def decode_bds_d2(buff,eph,utc):
  """
decode_bds_d2(const uint8_t *buff, eph_t *eph, double *utc"""

  result = librtk.decode_bds_d2(buff,eph,utc)


  return result

librtk.decode_gal_inav.argtypes = [ctypes.POINTER(ctypes.c_ubyte),ctypes.POINTER(eph_t),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
librtk.decode_gal_inav.restype = ctypes.c_int32
def decode_gal_inav(buff,eph,ion,utc):
  """
decode_gal_inav(const uint8_t *buff, eph_t *eph, double *ion,
                           double *utc"""

  result = librtk.decode_gal_inav(buff,eph,ion,utc)


  return result

librtk.decode_gal_fnav.argtypes = [ctypes.POINTER(ctypes.c_ubyte),ctypes.POINTER(eph_t),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
librtk.decode_gal_fnav.restype = ctypes.c_int32
def decode_gal_fnav(buff,eph,ion,utc):
  """
decode_gal_fnav(const uint8_t *buff, eph_t *eph, double *ion,
                           double *utc"""

  result = librtk.decode_gal_fnav(buff,eph,ion,utc)


  return result

librtk.decode_irn_nav.argtypes = [ctypes.POINTER(ctypes.c_ubyte),ctypes.POINTER(eph_t),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
librtk.decode_irn_nav.restype = ctypes.c_int32
def decode_irn_nav(buff,eph,ion,utc):
  """
decode_irn_nav(const uint8_t *buff, eph_t *eph, double *ion,
                          double *utc"""

  result = librtk.decode_irn_nav(buff,eph,ion,utc)


  return result

librtk.init_raw.argtypes = [ctypes.POINTER(raw_t),ctypes.c_int32]
librtk.init_raw.restype = ctypes.c_int32
def init_raw(raw,format):
  """
init_raw   (raw_t *raw, int format"""

  result = librtk.init_raw(raw,format)


  return result

librtk.free_raw.argtypes = [ctypes.POINTER(raw_t)]
librtk.free_raw.restype = ctypes.c_void_p
def free_raw(raw):
  """
free_raw  (raw_t *raw"""

  result = librtk.free_raw(raw)


  return result

librtk.input_raw.argtypes = [ctypes.POINTER(raw_t),ctypes.c_int32,ctypes.c_ubyte]
librtk.input_raw.restype = ctypes.c_int32
def input_raw(raw,format,data):
  """
input_raw  (raw_t *raw, int format, uint8_t data"""

  result = librtk.input_raw(raw,format,data)


  return result

librtk.input_rawf.argtypes = [ctypes.POINTER(raw_t),ctypes.c_int32,ctypes.POINTER(__sFILE)]
librtk.input_rawf.restype = ctypes.c_int32
def input_rawf(raw,format,fp):
  """
input_rawf (raw_t *raw, int format, FILE *fp"""

  result = librtk.input_rawf(raw,format,fp)


  return result

librtk.init_rt17.argtypes = [ctypes.POINTER(raw_t)]
librtk.init_rt17.restype = ctypes.c_int32
def init_rt17(raw):
  """
init_rt17  (raw_t *raw"""

  result = librtk.init_rt17(raw)


  return result

librtk.free_rt17.argtypes = [ctypes.POINTER(raw_t)]
librtk.free_rt17.restype = ctypes.c_void_p
def free_rt17(raw):
  """
free_rt17 (raw_t *raw"""

  result = librtk.free_rt17(raw)


  return result

librtk.input_oem4.argtypes = [ctypes.POINTER(raw_t),ctypes.c_ubyte]
librtk.input_oem4.restype = ctypes.c_int32
def input_oem4(raw,data):
  """
input_oem4  (raw_t *raw, uint8_t data"""

  result = librtk.input_oem4(raw,data)


  return result

librtk.input_oem3.argtypes = [ctypes.POINTER(raw_t),ctypes.c_ubyte]
librtk.input_oem3.restype = ctypes.c_int32
def input_oem3(raw,data):
  """
input_oem3  (raw_t *raw, uint8_t data"""

  result = librtk.input_oem3(raw,data)


  return result

librtk.input_ubx.argtypes = [ctypes.POINTER(raw_t),ctypes.c_ubyte]
librtk.input_ubx.restype = ctypes.c_int32
def input_ubx(raw,data):
  """
input_ubx   (raw_t *raw, uint8_t data"""

  result = librtk.input_ubx(raw,data)


  return result

librtk.input_ss2.argtypes = [ctypes.POINTER(raw_t),ctypes.c_ubyte]
librtk.input_ss2.restype = ctypes.c_int32
def input_ss2(raw,data):
  """
input_ss2   (raw_t *raw, uint8_t data"""

  result = librtk.input_ss2(raw,data)


  return result

librtk.input_cres.argtypes = [ctypes.POINTER(raw_t),ctypes.c_ubyte]
librtk.input_cres.restype = ctypes.c_int32
def input_cres(raw,data):
  """
input_cres  (raw_t *raw, uint8_t data"""

  result = librtk.input_cres(raw,data)


  return result

librtk.input_stq.argtypes = [ctypes.POINTER(raw_t),ctypes.c_ubyte]
librtk.input_stq.restype = ctypes.c_int32
def input_stq(raw,data):
  """
input_stq   (raw_t *raw, uint8_t data"""

  result = librtk.input_stq(raw,data)


  return result

librtk.input_javad.argtypes = [ctypes.POINTER(raw_t),ctypes.c_ubyte]
librtk.input_javad.restype = ctypes.c_int32
def input_javad(raw,data):
  """
input_javad (raw_t *raw, uint8_t data"""

  result = librtk.input_javad(raw,data)


  return result

librtk.input_nvs.argtypes = [ctypes.POINTER(raw_t),ctypes.c_ubyte]
librtk.input_nvs.restype = ctypes.c_int32
def input_nvs(raw,data):
  """
input_nvs   (raw_t *raw, uint8_t data"""

  result = librtk.input_nvs(raw,data)


  return result

librtk.input_bnx.argtypes = [ctypes.POINTER(raw_t),ctypes.c_ubyte]
librtk.input_bnx.restype = ctypes.c_int32
def input_bnx(raw,data):
  """
input_bnx   (raw_t *raw, uint8_t data"""

  result = librtk.input_bnx(raw,data)


  return result

librtk.input_rt17.argtypes = [ctypes.POINTER(raw_t),ctypes.c_ubyte]
librtk.input_rt17.restype = ctypes.c_int32
def input_rt17(raw,data):
  """
input_rt17  (raw_t *raw, uint8_t data"""

  result = librtk.input_rt17(raw,data)


  return result

librtk.input_sbf.argtypes = [ctypes.POINTER(raw_t),ctypes.c_ubyte]
librtk.input_sbf.restype = ctypes.c_int32
def input_sbf(raw,data):
  """
input_sbf   (raw_t *raw, uint8_t data"""

  result = librtk.input_sbf(raw,data)


  return result

librtk.input_oem4f.argtypes = [ctypes.POINTER(raw_t),ctypes.POINTER(__sFILE)]
librtk.input_oem4f.restype = ctypes.c_int32
def input_oem4f(raw,fp):
  """
input_oem4f (raw_t *raw, FILE *fp"""

  result = librtk.input_oem4f(raw,fp)


  return result

librtk.input_oem3f.argtypes = [ctypes.POINTER(raw_t),ctypes.POINTER(__sFILE)]
librtk.input_oem3f.restype = ctypes.c_int32
def input_oem3f(raw,fp):
  """
input_oem3f (raw_t *raw, FILE *fp"""

  result = librtk.input_oem3f(raw,fp)


  return result

librtk.input_ubxf.argtypes = [ctypes.POINTER(raw_t),ctypes.POINTER(__sFILE)]
librtk.input_ubxf.restype = ctypes.c_int32
def input_ubxf(raw,fp):
  """
input_ubxf  (raw_t *raw, FILE *fp"""

  result = librtk.input_ubxf(raw,fp)


  return result

librtk.input_ss2f.argtypes = [ctypes.POINTER(raw_t),ctypes.POINTER(__sFILE)]
librtk.input_ss2f.restype = ctypes.c_int32
def input_ss2f(raw,fp):
  """
input_ss2f  (raw_t *raw, FILE *fp"""

  result = librtk.input_ss2f(raw,fp)


  return result

librtk.input_cresf.argtypes = [ctypes.POINTER(raw_t),ctypes.POINTER(__sFILE)]
librtk.input_cresf.restype = ctypes.c_int32
def input_cresf(raw,fp):
  """
input_cresf (raw_t *raw, FILE *fp"""

  result = librtk.input_cresf(raw,fp)


  return result

librtk.input_stqf.argtypes = [ctypes.POINTER(raw_t),ctypes.POINTER(__sFILE)]
librtk.input_stqf.restype = ctypes.c_int32
def input_stqf(raw,fp):
  """
input_stqf  (raw_t *raw, FILE *fp"""

  result = librtk.input_stqf(raw,fp)


  return result

librtk.input_javadf.argtypes = [ctypes.POINTER(raw_t),ctypes.POINTER(__sFILE)]
librtk.input_javadf.restype = ctypes.c_int32
def input_javadf(raw,fp):
  """
input_javadf(raw_t *raw, FILE *fp"""

  result = librtk.input_javadf(raw,fp)


  return result

librtk.input_nvsf.argtypes = [ctypes.POINTER(raw_t),ctypes.POINTER(__sFILE)]
librtk.input_nvsf.restype = ctypes.c_int32
def input_nvsf(raw,fp):
  """
input_nvsf  (raw_t *raw, FILE *fp"""

  result = librtk.input_nvsf(raw,fp)


  return result

librtk.input_bnxf.argtypes = [ctypes.POINTER(raw_t),ctypes.POINTER(__sFILE)]
librtk.input_bnxf.restype = ctypes.c_int32
def input_bnxf(raw,fp):
  """
input_bnxf  (raw_t *raw, FILE *fp"""

  result = librtk.input_bnxf(raw,fp)


  return result

librtk.input_rt17f.argtypes = [ctypes.POINTER(raw_t),ctypes.POINTER(__sFILE)]
librtk.input_rt17f.restype = ctypes.c_int32
def input_rt17f(raw,fp):
  """
input_rt17f (raw_t *raw, FILE *fp"""

  result = librtk.input_rt17f(raw,fp)


  return result

librtk.input_sbff.argtypes = [ctypes.POINTER(raw_t),ctypes.POINTER(__sFILE)]
librtk.input_sbff.restype = ctypes.c_int32
def input_sbff(raw,fp):
  """
input_sbff  (raw_t *raw, FILE *fp"""

  result = librtk.input_sbff(raw,fp)


  return result

librtk.gen_ubx.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.POINTER(ctypes.c_ubyte)]
librtk.gen_ubx.restype = ctypes.c_int32
def gen_ubx(msg,buff):
  """
gen_ubx (const char *msg, uint8_t *buff"""

  result = librtk.gen_ubx(msg,buff)


  return result

librtk.gen_stq.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.POINTER(ctypes.c_ubyte)]
librtk.gen_stq.restype = ctypes.c_int32
def gen_stq(msg,buff):
  """
gen_stq (const char *msg, uint8_t *buff"""

  result = librtk.gen_stq(msg,buff)


  return result

librtk.gen_nvs.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.POINTER(ctypes.c_ubyte)]
librtk.gen_nvs.restype = ctypes.c_int32
def gen_nvs(msg,buff):
  """
gen_nvs (const char *msg, uint8_t *buff"""

  result = librtk.gen_nvs(msg,buff)


  return result

librtk.init_rtcm.argtypes = [ctypes.POINTER(rtcm_t)]
librtk.init_rtcm.restype = ctypes.c_int32
def init_rtcm(rtcm):
  """
init_rtcm   (rtcm_t *rtcm"""

  result = librtk.init_rtcm(rtcm)


  return result

librtk.free_rtcm.argtypes = [ctypes.POINTER(rtcm_t)]
librtk.free_rtcm.restype = ctypes.c_void_p
def free_rtcm(rtcm):
  """
free_rtcm  (rtcm_t *rtcm"""

  result = librtk.free_rtcm(rtcm)


  return result

librtk.input_rtcm2.argtypes = [ctypes.POINTER(rtcm_t),ctypes.c_ubyte]
librtk.input_rtcm2.restype = ctypes.c_int32
def input_rtcm2(rtcm,data):
  """
input_rtcm2 (rtcm_t *rtcm, uint8_t data"""

  result = librtk.input_rtcm2(rtcm,data)


  return result

librtk.input_rtcm3.argtypes = [ctypes.POINTER(rtcm_t),ctypes.c_ubyte]
librtk.input_rtcm3.restype = ctypes.c_int32
def input_rtcm3(rtcm,data):
  """
input_rtcm3 (rtcm_t *rtcm, uint8_t data"""

  result = librtk.input_rtcm3(rtcm,data)


  return result

librtk.input_rtcm2f.argtypes = [ctypes.POINTER(rtcm_t),ctypes.POINTER(__sFILE)]
librtk.input_rtcm2f.restype = ctypes.c_int32
def input_rtcm2f(rtcm,fp):
  """
input_rtcm2f(rtcm_t *rtcm, FILE *fp"""

  result = librtk.input_rtcm2f(rtcm,fp)


  return result

librtk.input_rtcm3f.argtypes = [ctypes.POINTER(rtcm_t),ctypes.POINTER(__sFILE)]
librtk.input_rtcm3f.restype = ctypes.c_int32
def input_rtcm3f(rtcm,fp):
  """
input_rtcm3f(rtcm_t *rtcm, FILE *fp"""

  result = librtk.input_rtcm3f(rtcm,fp)


  return result

librtk.gen_rtcm2.argtypes = [ctypes.POINTER(rtcm_t),ctypes.c_int32,ctypes.c_int32]
librtk.gen_rtcm2.restype = ctypes.c_int32
def gen_rtcm2(rtcm,type,sync):
  """
gen_rtcm2   (rtcm_t *rtcm, int type, int sync"""

  result = librtk.gen_rtcm2(rtcm,type,sync)


  return result

librtk.gen_rtcm3.argtypes = [ctypes.POINTER(rtcm_t),ctypes.c_int32,ctypes.c_int32,ctypes.c_int32]
librtk.gen_rtcm3.restype = ctypes.c_int32
def gen_rtcm3(rtcm,type,subtype,sync):
  """
gen_rtcm3   (rtcm_t *rtcm, int type, int subtype, int sync"""

  result = librtk.gen_rtcm3(rtcm,type,subtype,sync)


  return result

librtk.initsolbuf.argtypes = [ctypes.POINTER(solbuf_t),ctypes.c_int32,ctypes.c_int32]
librtk.initsolbuf.restype = ctypes.c_void_p
def initsolbuf(solbuf,cyclic,nmax):
  """
initsolbuf(solbuf_t *solbuf, int cyclic, int nmax"""

  result = librtk.initsolbuf(solbuf,cyclic,nmax)


  return result

librtk.freesolbuf.argtypes = [ctypes.POINTER(solbuf_t)]
librtk.freesolbuf.restype = ctypes.c_void_p
def freesolbuf(solbuf):
  """
freesolbuf(solbuf_t *solbuf"""

  result = librtk.freesolbuf(solbuf)


  return result

librtk.freesolstatbuf.argtypes = [ctypes.POINTER(solstatbuf_t)]
librtk.freesolstatbuf.restype = ctypes.c_void_p
def freesolstatbuf(solstatbuf):
  """
freesolstatbuf(solstatbuf_t *solstatbuf"""

  result = librtk.freesolstatbuf(solstatbuf)


  return result

librtk.getsol.argtypes = [ctypes.POINTER(solbuf_t),ctypes.c_int32]
librtk.getsol.restype = ctypes.POINTER(sol_t)
def getsol(solbuf,index):
  """
getsol(solbuf_t *solbuf, int index"""

  result = librtk.getsol(solbuf,index)


  return result

librtk.addsol.argtypes = [ctypes.POINTER(solbuf_t),ctypes.POINTER(sol_t)]
librtk.addsol.restype = ctypes.c_int32
def addsol(solbuf,sol):
  """
addsol(solbuf_t *solbuf, const sol_t *sol"""

  result = librtk.addsol(solbuf,sol)


  return result

librtk.inputsol.argtypes = [ctypes.c_ubyte,gtime_t,gtime_t,ctypes.c_double,ctypes.c_int32,ctypes.POINTER(solopt_t),ctypes.POINTER(solbuf_t)]
librtk.inputsol.restype = ctypes.c_int32
def inputsol(data,ts,te,tint,qflag,opt,solbuf):
  """
inputsol(uint8_t data, gtime_t ts, gtime_t te, double tint,
                    int qflag, const solopt_t *opt, solbuf_t *solbuf"""

  result = librtk.inputsol(data,ts,te,tint,qflag,opt,solbuf)


  return result

librtk.outprcopts.argtypes = [ctypes.POINTER(ctypes.c_ubyte),ctypes.POINTER(prcopt_t)]
librtk.outprcopts.restype = ctypes.c_int32
def outprcopts(buff,opt):
  """
outprcopts(uint8_t *buff, const prcopt_t *opt"""

  result = librtk.outprcopts(buff,opt)


  return result

librtk.outsolheads.argtypes = [ctypes.POINTER(ctypes.c_ubyte),ctypes.POINTER(solopt_t)]
librtk.outsolheads.restype = ctypes.c_int32
def outsolheads(buff,opt):
  """
outsolheads(uint8_t *buff, const solopt_t *opt"""

  result = librtk.outsolheads(buff,opt)


  return result

librtk.outsols.argtypes = [ctypes.POINTER(ctypes.c_ubyte),ctypes.POINTER(sol_t),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(solopt_t)]
librtk.outsols.restype = ctypes.c_int32
def outsols(buff,sol,rb,opt):
  """
outsols  (uint8_t *buff, const sol_t *sol, const double *rb,
                     const solopt_t *opt"""

  result = librtk.outsols(buff,sol,rb,opt)


  return result

librtk.outsolexs.argtypes = [ctypes.POINTER(ctypes.c_ubyte),ctypes.POINTER(sol_t),ctypes.POINTER(ssat_t),ctypes.POINTER(solopt_t)]
librtk.outsolexs.restype = ctypes.c_int32
def outsolexs(buff,sol,ssat,opt):
  """
outsolexs(uint8_t *buff, const sol_t *sol, const ssat_t *ssat,
                     const solopt_t *opt"""

  result = librtk.outsolexs(buff,sol,ssat,opt)


  return result

librtk.outprcopt.argtypes = [ctypes.POINTER(__sFILE),ctypes.POINTER(prcopt_t)]
librtk.outprcopt.restype = ctypes.c_void_p
def outprcopt(fp,opt):
  """
outprcopt(FILE *fp, const prcopt_t *opt"""

  result = librtk.outprcopt(fp,opt)


  return result

librtk.outsolhead.argtypes = [ctypes.POINTER(__sFILE),ctypes.POINTER(solopt_t)]
librtk.outsolhead.restype = ctypes.c_void_p
def outsolhead(fp,opt):
  """
outsolhead(FILE *fp, const solopt_t *opt"""

  result = librtk.outsolhead(fp,opt)


  return result

librtk.outsol.argtypes = [ctypes.POINTER(__sFILE),ctypes.POINTER(sol_t),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(solopt_t)]
librtk.outsol.restype = ctypes.c_void_p
def outsol(fp,sol,rb,opt):
  """
outsol  (FILE *fp, const sol_t *sol, const double *rb,
                     const solopt_t *opt"""

  result = librtk.outsol(fp,sol,rb,opt)


  return result

librtk.outsolex.argtypes = [ctypes.POINTER(__sFILE),ctypes.POINTER(sol_t),ctypes.POINTER(ssat_t),ctypes.POINTER(solopt_t)]
librtk.outsolex.restype = ctypes.c_void_p
def outsolex(fp,sol,ssat,opt):
  """
outsolex(FILE *fp, const sol_t *sol, const ssat_t *ssat,
                     const solopt_t *opt"""

  result = librtk.outsolex(fp,sol,ssat,opt)


  return result

librtk.outnmea_rmc.argtypes = [ctypes.POINTER(ctypes.c_ubyte),ctypes.POINTER(sol_t)]
librtk.outnmea_rmc.restype = ctypes.c_int32
def outnmea_rmc(buff,sol):
  """
outnmea_rmc(uint8_t *buff, const sol_t *sol"""

  result = librtk.outnmea_rmc(buff,sol)


  return result

librtk.outnmea_gga.argtypes = [ctypes.POINTER(ctypes.c_ubyte),ctypes.POINTER(sol_t)]
librtk.outnmea_gga.restype = ctypes.c_int32
def outnmea_gga(buff,sol):
  """
outnmea_gga(uint8_t *buff, const sol_t *sol"""

  result = librtk.outnmea_gga(buff,sol)


  return result

librtk.outnmea_gsa.argtypes = [ctypes.POINTER(ctypes.c_ubyte),ctypes.POINTER(sol_t),ctypes.POINTER(ssat_t)]
librtk.outnmea_gsa.restype = ctypes.c_int32
def outnmea_gsa(buff,sol,ssat):
  """
outnmea_gsa(uint8_t *buff, const sol_t *sol,
                       const ssat_t *ssat"""

  result = librtk.outnmea_gsa(buff,sol,ssat)


  return result

librtk.outnmea_gsv.argtypes = [ctypes.POINTER(ctypes.c_ubyte),ctypes.POINTER(sol_t),ctypes.POINTER(ssat_t)]
librtk.outnmea_gsv.restype = ctypes.c_int32
def outnmea_gsv(buff,sol,ssat):
  """
outnmea_gsv(uint8_t *buff, const sol_t *sol,
                       const ssat_t *ssat"""

  result = librtk.outnmea_gsv(buff,sol,ssat)


  return result

librtk.convkml.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.POINTER(ctypes.c_char),gtime_t,gtime_t,ctypes.c_double,ctypes.c_int32,ctypes.POINTER(ctypes.c_double),ctypes.c_int32,ctypes.c_int32,ctypes.c_int32,ctypes.c_int32]
librtk.convkml.restype = ctypes.c_int32
def convkml(infile,outfile,ts,te,tint,qflg,offset,tcolor,pcolor,outalt,outtime):
  """
convkml(const char *infile, const char *outfile, gtime_t ts,
                   gtime_t te, double tint, int qflg, double *offset,
                   int tcolor, int pcolor, int outalt, int outtime"""

  result = librtk.convkml(infile,outfile,ts,te,tint,qflg,offset,tcolor,pcolor,outalt,outtime)


  return result

librtk.convgpx.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.POINTER(ctypes.c_char),gtime_t,gtime_t,ctypes.c_double,ctypes.c_int32,ctypes.POINTER(ctypes.c_double),ctypes.c_int32,ctypes.c_int32,ctypes.c_int32,ctypes.c_int32]
librtk.convgpx.restype = ctypes.c_int32
def convgpx(infile,outfile,ts,te,tint,qflg,offset,outtrk,outpnt,outalt,outtime):
  """
convgpx(const char *infile, const char *outfile, gtime_t ts,
                   gtime_t te, double tint, int qflg, double *offset,
                   int outtrk, int outpnt, int outalt, int outtime"""

  result = librtk.convgpx(infile,outfile,ts,te,tint,qflg,offset,outtrk,outpnt,outalt,outtime)


  return result

librtk.sbsreadmsg.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.c_int32,ctypes.POINTER(sbs_t)]
librtk.sbsreadmsg.restype = ctypes.c_int32
def sbsreadmsg(file,sel,sbs):
  """
sbsreadmsg (const char *file, int sel, sbs_t *sbs"""

  result = librtk.sbsreadmsg(file,sel,sbs)


  return result

librtk.sbsreadmsgt.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.c_int32,gtime_t,gtime_t,ctypes.POINTER(sbs_t)]
librtk.sbsreadmsgt.restype = ctypes.c_int32
def sbsreadmsgt(file,sel,ts,te,sbs):
  """
sbsreadmsgt(const char *file, int sel, gtime_t ts, gtime_t te,
                        sbs_t *sbs"""

  result = librtk.sbsreadmsgt(file,sel,ts,te,sbs)


  return result

librtk.sbsoutmsg.argtypes = [ctypes.POINTER(__sFILE),ctypes.POINTER(sbsmsg_t)]
librtk.sbsoutmsg.restype = ctypes.c_void_p
def sbsoutmsg(fp,sbsmsg):
  """
sbsoutmsg(FILE *fp, sbsmsg_t *sbsmsg"""

  result = librtk.sbsoutmsg(fp,sbsmsg)


  return result

librtk.sbsdecodemsg.argtypes = [gtime_t,ctypes.c_int32,ctypes.POINTER(ctypes.c_uint32),ctypes.POINTER(sbsmsg_t)]
librtk.sbsdecodemsg.restype = ctypes.c_int32
def sbsdecodemsg(time,prn,words,sbsmsg):
  """
sbsdecodemsg(gtime_t time, int prn, const uint32_t *words,
                         sbsmsg_t *sbsmsg"""

  result = librtk.sbsdecodemsg(time,prn,words,sbsmsg)


  return result

librtk.sbsupdatecorr.argtypes = [ctypes.POINTER(sbsmsg_t),ctypes.POINTER(nav_t)]
librtk.sbsupdatecorr.restype = ctypes.c_int32
def sbsupdatecorr(msg,nav):
  """
sbsupdatecorr(const sbsmsg_t *msg, nav_t *nav"""

  result = librtk.sbsupdatecorr(msg,nav)


  return result

librtk.sbssatcorr.argtypes = [gtime_t,ctypes.c_int32,ctypes.POINTER(nav_t),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
librtk.sbssatcorr.restype = ctypes.c_int32
def sbssatcorr(time,sat,nav,rs,dts,var):
  """
sbssatcorr(gtime_t time, int sat, const nav_t *nav, double *rs,
                      double *dts, double *var"""

  result = librtk.sbssatcorr(time,sat,nav,rs,dts,var)


  return result

librtk.sbsioncorr.argtypes = [gtime_t,ctypes.POINTER(nav_t),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
librtk.sbsioncorr.restype = ctypes.c_int32
def sbsioncorr(time,nav,pos,azel,delay,var):
  """
sbsioncorr(gtime_t time, const nav_t *nav, const double *pos,
                      const double *azel, double *delay, double *var"""

  result = librtk.sbsioncorr(time,nav,pos,azel,delay,var)


  return result

librtk.sbstropcorr.argtypes = [gtime_t,ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
librtk.sbstropcorr.restype = ctypes.c_double
def sbstropcorr(time,pos,azel,var):
  """
sbstropcorr(gtime_t time, const double *pos, const double *azel,
                          double *var"""

  result = librtk.sbstropcorr(time,pos,azel,var)


  return result

librtk.searchopt.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.POINTER(opt_t)]
librtk.searchopt.restype = ctypes.POINTER(opt_t)
def searchopt(name,opts):
  """
searchopt(const char *name, const opt_t *opts"""

  result = librtk.searchopt(name,opts)


  return result

librtk.str2opt.argtypes = [ctypes.POINTER(opt_t),ctypes.POINTER(ctypes.c_char)]
librtk.str2opt.restype = ctypes.c_int32
def str2opt(opt,str):
  """
str2opt(opt_t *opt, const char *str"""

  result = librtk.str2opt(opt,str)


  return result

librtk.opt2str.argtypes = [ctypes.POINTER(opt_t),ctypes.POINTER(ctypes.c_char)]
librtk.opt2str.restype = ctypes.c_int32
def opt2str(opt,str):
  """
opt2str(const opt_t *opt, char *str"""

  result = librtk.opt2str(opt,str)


  return result

librtk.opt2buf.argtypes = [ctypes.POINTER(opt_t),ctypes.POINTER(ctypes.c_char)]
librtk.opt2buf.restype = ctypes.c_int32
def opt2buf(opt,buff):
  """
opt2buf(const opt_t *opt, char *buff"""

  result = librtk.opt2buf(opt,buff)


  return result

librtk.loadopts.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.POINTER(opt_t)]
librtk.loadopts.restype = ctypes.c_int32
def loadopts(file,opts):
  """
loadopts(const char *file, opt_t *opts"""

  result = librtk.loadopts(file,opts)


  return result

librtk.saveopts.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.POINTER(ctypes.c_char),ctypes.POINTER(ctypes.c_char),ctypes.POINTER(opt_t)]
librtk.saveopts.restype = ctypes.c_int32
def saveopts(file,mode,comment,opts):
  """
saveopts(const char *file, const char *mode, const char *comment,
                    const opt_t *opts"""

  result = librtk.saveopts(file,mode,comment,opts)


  return result

librtk.resetsysopts.argtypes = []
librtk.resetsysopts.restype = ctypes.c_void_p
def resetsysopts():
  """
resetsysopts(void"""

  result = librtk.resetsysopts()


  return result

librtk.getsysopts.argtypes = [ctypes.POINTER(prcopt_t),ctypes.POINTER(solopt_t),ctypes.POINTER(filopt_t)]
librtk.getsysopts.restype = ctypes.c_void_p
def getsysopts(popt,sopt,fopt):
  """
getsysopts(prcopt_t *popt, solopt_t *sopt, filopt_t *fopt"""

  result = librtk.getsysopts(popt,sopt,fopt)


  return result

librtk.setsysopts.argtypes = [ctypes.POINTER(prcopt_t),ctypes.POINTER(solopt_t),ctypes.POINTER(filopt_t)]
librtk.setsysopts.restype = ctypes.c_void_p
def setsysopts(popt,sopt,fopt):
  """
setsysopts(const prcopt_t *popt, const solopt_t *sopt,
                       const filopt_t *fopt"""

  result = librtk.setsysopts(popt,sopt,fopt)


  return result

librtk.strinitcom.argtypes = []
librtk.strinitcom.restype = ctypes.c_void_p
def strinitcom():
  """
strinitcom(void"""

  result = librtk.strinitcom()


  return result

librtk.strinit.argtypes = [ctypes.POINTER(stream_t)]
librtk.strinit.restype = ctypes.c_void_p
def strinit(stream):
  """
strinit  (stream_t *stream"""

  result = librtk.strinit(stream)


  return result

librtk.strlock.argtypes = [ctypes.POINTER(stream_t)]
librtk.strlock.restype = ctypes.c_void_p
def strlock(stream):
  """
strlock  (stream_t *stream"""

  result = librtk.strlock(stream)


  return result

librtk.strunlock.argtypes = [ctypes.POINTER(stream_t)]
librtk.strunlock.restype = ctypes.c_void_p
def strunlock(stream):
  """
strunlock(stream_t *stream"""

  result = librtk.strunlock(stream)


  return result

librtk.stropen.argtypes = [ctypes.POINTER(stream_t),ctypes.c_int32,ctypes.c_int32,ctypes.POINTER(ctypes.c_char)]
librtk.stropen.restype = ctypes.c_int32
def stropen(stream,type,mode,path):
  """
stropen  (stream_t *stream, int type, int mode, const char *path"""

  result = librtk.stropen(stream,type,mode,path)


  return result

librtk.strclose.argtypes = [ctypes.POINTER(stream_t)]
librtk.strclose.restype = ctypes.c_void_p
def strclose(stream):
  """
strclose (stream_t *stream"""

  result = librtk.strclose(stream)


  return result

librtk.strread.argtypes = [ctypes.POINTER(stream_t),ctypes.POINTER(ctypes.c_ubyte),ctypes.c_int32]
librtk.strread.restype = ctypes.c_int32
def strread(stream,buff,n):
  """
strread  (stream_t *stream, uint8_t *buff, int n"""

  result = librtk.strread(stream,buff,n)


  return result

librtk.strwrite.argtypes = [ctypes.POINTER(stream_t),ctypes.POINTER(ctypes.c_ubyte),ctypes.c_int32]
librtk.strwrite.restype = ctypes.c_int32
def strwrite(stream,buff,n):
  """
strwrite (stream_t *stream, uint8_t *buff, int n"""

  result = librtk.strwrite(stream,buff,n)


  return result

librtk.strsync.argtypes = [ctypes.POINTER(stream_t),ctypes.POINTER(stream_t)]
librtk.strsync.restype = ctypes.c_void_p
def strsync(stream1,stream2):
  """
strsync  (stream_t *stream1, stream_t *stream2"""

  result = librtk.strsync(stream1,stream2)


  return result

librtk.strstat.argtypes = [ctypes.POINTER(stream_t),ctypes.POINTER(ctypes.c_char)]
librtk.strstat.restype = ctypes.c_int32
def strstat(stream,msg):
  """
strstat  (stream_t *stream, char *msg"""

  result = librtk.strstat(stream,msg)


  return result

librtk.strstatx.argtypes = [ctypes.POINTER(stream_t),ctypes.POINTER(ctypes.c_char)]
librtk.strstatx.restype = ctypes.c_int32
def strstatx(stream,msg):
  """
strstatx (stream_t *stream, char *msg"""

  result = librtk.strstatx(stream,msg)


  return result

librtk.strsum.argtypes = [ctypes.POINTER(stream_t),ctypes.POINTER(ctypes.c_int32),ctypes.POINTER(ctypes.c_int32),ctypes.POINTER(ctypes.c_int32),ctypes.POINTER(ctypes.c_int32)]
librtk.strsum.restype = ctypes.c_void_p
def strsum(stream,inb,inr,outb,outr):
  """
strsum   (stream_t *stream, int *inb, int *inr, int *outb, int *outr"""

  result = librtk.strsum(stream,inb,inr,outb,outr)


  return result

librtk.strsetopt.argtypes = [ctypes.POINTER(ctypes.c_int32)]
librtk.strsetopt.restype = ctypes.c_void_p
def strsetopt(opt):
  """
strsetopt(const int *opt"""

  result = librtk.strsetopt(opt)


  return result

librtk.strgettime.argtypes = [ctypes.POINTER(stream_t)]
librtk.strgettime.restype = gtime_t
def strgettime(stream):
  """
strgettime(stream_t *stream"""

  result = librtk.strgettime(stream)


  return result

librtk.strsendnmea.argtypes = [ctypes.POINTER(stream_t),ctypes.POINTER(sol_t)]
librtk.strsendnmea.restype = ctypes.c_void_p
def strsendnmea(stream,sol):
  """
strsendnmea(stream_t *stream, const sol_t *sol"""

  result = librtk.strsendnmea(stream,sol)


  return result

librtk.strsendcmd.argtypes = [ctypes.POINTER(stream_t),ctypes.POINTER(ctypes.c_char)]
librtk.strsendcmd.restype = ctypes.c_void_p
def strsendcmd(stream,cmd):
  """
strsendcmd(stream_t *stream, const char *cmd"""

  result = librtk.strsendcmd(stream,cmd)


  return result

librtk.strsettimeout.argtypes = [ctypes.POINTER(stream_t),ctypes.c_int32,ctypes.c_int32]
librtk.strsettimeout.restype = ctypes.c_void_p
def strsettimeout(stream,toinact,tirecon):
  """
strsettimeout(stream_t *stream, int toinact, int tirecon"""

  result = librtk.strsettimeout(stream,toinact,tirecon)


  return result

librtk.strsetdir.argtypes = [ctypes.POINTER(ctypes.c_char)]
librtk.strsetdir.restype = ctypes.c_void_p
def strsetdir(dir):
  """
strsetdir(const char *dir"""

  result = librtk.strsetdir(dir)


  return result

librtk.strsetproxy.argtypes = [ctypes.POINTER(ctypes.c_char)]
librtk.strsetproxy.restype = ctypes.c_void_p
def strsetproxy(addr):
  """
strsetproxy(const char *addr"""

  result = librtk.strsetproxy(addr)


  return result

librtk.lambda_reduction.argtypes = [ctypes.c_int32,ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
librtk.lambda_reduction.restype = ctypes.c_int32
def lambda_reduction(n,Q,Z):
  """
lambda_reduction(int n, const double *Q, double *Z"""

  result = librtk.lambda_reduction(n,Q,Z)


  return result

librtk.lambda_search.argtypes = [ctypes.c_int32,ctypes.c_int32,ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
librtk.lambda_search.restype = ctypes.c_int32
def lambda_search(n,m,a,Q,F,s):
  """
lambda_search(int n, int m, const double *a, const double *Q,
                         double *F, double *s"""

  result = librtk.lambda_search(n,m,a,Q,F,s)


  return result

librtk.pntpos.argtypes = [ctypes.POINTER(obsd_t),ctypes.c_int32,ctypes.POINTER(nav_t),ctypes.POINTER(prcopt_t),ctypes.POINTER(sol_t),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ssat_t),ctypes.POINTER(ctypes.c_char)]
librtk.pntpos.restype = ctypes.c_int32
def pntpos(obs,n,nav,opt,sol,azel,ssat,msg):
  """
pntpos(const obsd_t *obs, int n, const nav_t *nav,
                  const prcopt_t *opt, sol_t *sol, double *azel,
                  ssat_t *ssat, char *msg"""

  result = librtk.pntpos(obs,n,nav,opt,sol,azel,ssat,msg)


  return result

librtk.rtkinit.argtypes = [ctypes.POINTER(rtk_t),ctypes.POINTER(prcopt_t)]
librtk.rtkinit.restype = ctypes.c_void_p
def rtkinit(rtk,opt):
  """
rtkinit(rtk_t *rtk, const prcopt_t *opt"""

  result = librtk.rtkinit(rtk,opt)


  return result

librtk.rtkfree.argtypes = [ctypes.POINTER(rtk_t)]
librtk.rtkfree.restype = ctypes.c_void_p
def rtkfree(rtk):
  """
rtkfree(rtk_t *rtk"""

  result = librtk.rtkfree(rtk)


  return result

librtk.rtkpos.argtypes = [ctypes.POINTER(rtk_t),ctypes.POINTER(obsd_t),ctypes.c_int32,ctypes.POINTER(nav_t)]
librtk.rtkpos.restype = ctypes.c_int32
def rtkpos(rtk,obs,nobs,nav):
  """
rtkpos (rtk_t *rtk, const obsd_t *obs, int nobs, const nav_t *nav"""

  result = librtk.rtkpos(rtk,obs,nobs,nav)


  return result

librtk.rtkopenstat.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.c_int32]
librtk.rtkopenstat.restype = ctypes.c_int32
def rtkopenstat(file,level):
  """
rtkopenstat(const char *file, int level"""

  result = librtk.rtkopenstat(file,level)


  return result

librtk.rtkclosestat.argtypes = []
librtk.rtkclosestat.restype = ctypes.c_void_p
def rtkclosestat():
  """
rtkclosestat(void"""

  result = librtk.rtkclosestat()


  return result

librtk.rtkoutstat.argtypes = [ctypes.POINTER(rtk_t),ctypes.POINTER(ctypes.c_char)]
librtk.rtkoutstat.restype = ctypes.c_int32
def rtkoutstat(rtk,buff):
  """
rtkoutstat(rtk_t *rtk, char *buff"""

  result = librtk.rtkoutstat(rtk,buff)


  return result

librtk.pppos.argtypes = [ctypes.POINTER(rtk_t),ctypes.POINTER(obsd_t),ctypes.c_int32,ctypes.POINTER(nav_t)]
librtk.pppos.restype = ctypes.c_void_p
def pppos(rtk,obs,n,nav):
  """
pppos(rtk_t *rtk, const obsd_t *obs, int n, const nav_t *nav"""

  result = librtk.pppos(rtk,obs,n,nav)


  return result

librtk.pppnx.argtypes = [ctypes.POINTER(prcopt_t)]
librtk.pppnx.restype = ctypes.c_int32
def pppnx(opt):
  """
pppnx(const prcopt_t *opt"""

  result = librtk.pppnx(opt)


  return result

librtk.pppoutstat.argtypes = [ctypes.POINTER(rtk_t),ctypes.POINTER(ctypes.c_char)]
librtk.pppoutstat.restype = ctypes.c_int32
def pppoutstat(rtk,buff):
  """
pppoutstat(rtk_t *rtk, char *buff"""

  result = librtk.pppoutstat(rtk,buff)


  return result

librtk.ppp_ar.argtypes = [ctypes.POINTER(rtk_t),ctypes.POINTER(obsd_t),ctypes.c_int32,ctypes.POINTER(ctypes.c_int32),ctypes.POINTER(nav_t),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]
librtk.ppp_ar.restype = ctypes.c_int32
def ppp_ar(rtk,obs,n,exc,nav,azel,x,P):
  """
ppp_ar(rtk_t *rtk, const obsd_t *obs, int n, int *exc,
                  const nav_t *nav, const double *azel, double *x, double *P"""

  result = librtk.ppp_ar(rtk,obs,n,exc,nav,azel,x,P)


  return result

librtk.postpos.argtypes = [gtime_t,gtime_t,ctypes.c_double,ctypes.c_double,ctypes.POINTER(prcopt_t),ctypes.POINTER(solopt_t),ctypes.POINTER(filopt_t),ctypes.POINTER(ctypes.c_char),ctypes.c_int32,ctypes.POINTER(ctypes.c_char),ctypes.POINTER(ctypes.c_char),ctypes.POINTER(ctypes.c_char)]
librtk.postpos.restype = ctypes.c_int32
def postpos(ts,te,ti,tu,popt,sopt,fopt,infile,n,outfile,rov,base):
  """
postpos(gtime_t ts, gtime_t te, double ti, double tu,
                   const prcopt_t *popt, const solopt_t *sopt,
                   const filopt_t *fopt, char **infile, int n, char *outfile,
                   const char *rov, const char *base"""

  result = librtk.postpos(ts,te,ti,tu,popt,sopt,fopt,infile,n,outfile,rov,base)


  return result

librtk.strsvrinit.argtypes = [ctypes.POINTER(strsvr_t),ctypes.c_int32]
librtk.strsvrinit.restype = ctypes.c_void_p
def strsvrinit(svr,nout):
  """
strsvrinit (strsvr_t *svr, int nout"""

  result = librtk.strsvrinit(svr,nout)


  return result

librtk.strsvrstart.argtypes = [ctypes.POINTER(strsvr_t),ctypes.POINTER(ctypes.c_int32),ctypes.POINTER(ctypes.c_int32),ctypes.POINTER(ctypes.c_char),ctypes.POINTER(ctypes.c_char),ctypes.POINTER(strconv_t),ctypes.POINTER(ctypes.c_char),ctypes.POINTER(ctypes.c_char),ctypes.POINTER(ctypes.c_double)]
librtk.strsvrstart.restype = ctypes.c_int32
def strsvrstart(svr,opts,strs,paths,logs,conv,cmds,cmds_priodic,nmeapos):
  """
strsvrstart(strsvr_t *svr, int *opts, int *strs, char **paths,
                        char **logs, strconv_t **conv, char **cmds,
                        char **cmds_priodic, const double *nmeapos"""

  result = librtk.strsvrstart(svr,opts,strs,paths,logs,conv,cmds,cmds_priodic,nmeapos)


  return result

librtk.strsvrstop.argtypes = [ctypes.POINTER(strsvr_t),ctypes.POINTER(ctypes.c_char)]
librtk.strsvrstop.restype = ctypes.c_void_p
def strsvrstop(svr,cmds):
  """
strsvrstop (strsvr_t *svr, char **cmds"""

  result = librtk.strsvrstop(svr,cmds)


  return result

librtk.strsvrstat.argtypes = [ctypes.POINTER(strsvr_t),ctypes.POINTER(ctypes.c_int32),ctypes.POINTER(ctypes.c_int32),ctypes.POINTER(ctypes.c_int32),ctypes.POINTER(ctypes.c_int32),ctypes.POINTER(ctypes.c_char)]
librtk.strsvrstat.restype = ctypes.c_void_p
def strsvrstat(svr,stat,log_stat,byte,bps,msg):
  """
strsvrstat (strsvr_t *svr, int *stat, int *log_stat, int *byte,
                        int *bps, char *msg"""

  result = librtk.strsvrstat(svr,stat,log_stat,byte,bps,msg)


  return result

librtk.strconvnew.argtypes = [ctypes.c_int32,ctypes.c_int32,ctypes.POINTER(ctypes.c_char),ctypes.c_int32,ctypes.c_int32,ctypes.POINTER(ctypes.c_char)]
librtk.strconvnew.restype = ctypes.POINTER(strconv_t)
def strconvnew(itype,otype,msgs,staid,stasel,opt):
  """
strconvnew(int itype, int otype, const char *msgs, int staid,
                             int stasel, const char *opt"""

  result = librtk.strconvnew(itype,otype,msgs,staid,stasel,opt)


  return result

librtk.strconvfree.argtypes = [ctypes.POINTER(strconv_t)]
librtk.strconvfree.restype = ctypes.c_void_p
def strconvfree(conv):
  """
strconvfree(strconv_t *conv"""

  result = librtk.strconvfree(conv)


  return result

librtk.rtksvrinit.argtypes = [ctypes.POINTER(rtksvr_t)]
librtk.rtksvrinit.restype = ctypes.c_int32
def rtksvrinit(svr):
  """
rtksvrinit  (rtksvr_t *svr"""

  result = librtk.rtksvrinit(svr)


  return result

librtk.rtksvrfree.argtypes = [ctypes.POINTER(rtksvr_t)]
librtk.rtksvrfree.restype = ctypes.c_void_p
def rtksvrfree(svr):
  """
rtksvrfree  (rtksvr_t *svr"""

  result = librtk.rtksvrfree(svr)


  return result

librtk.rtksvrstart.argtypes = [ctypes.POINTER(rtksvr_t),ctypes.c_int32,ctypes.c_int32,ctypes.POINTER(ctypes.c_int32),ctypes.POINTER(ctypes.c_char),ctypes.POINTER(ctypes.c_int32),ctypes.c_int32,ctypes.POINTER(ctypes.c_char),ctypes.POINTER(ctypes.c_char),ctypes.POINTER(ctypes.c_char),ctypes.c_int32,ctypes.c_int32,ctypes.POINTER(ctypes.c_double),ctypes.POINTER(prcopt_t),ctypes.POINTER(solopt_t),ctypes.POINTER(stream_t),ctypes.POINTER(ctypes.c_char)]
librtk.rtksvrstart.restype = ctypes.c_int32
def rtksvrstart(svr,cycle,buffsize,strs,paths,formats,navsel,cmds,cmds_periodic,rcvopts,nmeacycle,nmeareq,nmeapos,prcopt,solopt,moni,errmsg):
  """
rtksvrstart (rtksvr_t *svr, int cycle, int buffsize, int *strs,
                         char **paths, int *formats, int navsel, char **cmds,
                         char **cmds_periodic, char **rcvopts, int nmeacycle,
                         int nmeareq, const double *nmeapos, prcopt_t *prcopt,
                         solopt_t *solopt, stream_t *moni, char *errmsg"""

  result = librtk.rtksvrstart(svr,cycle,buffsize,strs,paths,formats,navsel,cmds,cmds_periodic,rcvopts,nmeacycle,nmeareq,nmeapos,prcopt,solopt,moni,errmsg)


  return result

librtk.rtksvrstop.argtypes = [ctypes.POINTER(rtksvr_t),ctypes.POINTER(ctypes.c_char)]
librtk.rtksvrstop.restype = ctypes.c_void_p
def rtksvrstop(svr,cmds):
  """
rtksvrstop  (rtksvr_t *svr, char **cmds"""

  result = librtk.rtksvrstop(svr,cmds)


  return result

librtk.rtksvropenstr.argtypes = [ctypes.POINTER(rtksvr_t),ctypes.c_int32,ctypes.c_int32,ctypes.POINTER(ctypes.c_char),ctypes.POINTER(solopt_t)]
librtk.rtksvropenstr.restype = ctypes.c_int32
def rtksvropenstr(svr,index,str,path,solopt):
  """
rtksvropenstr(rtksvr_t *svr, int index, int str, const char *path,
                          const solopt_t *solopt"""

  result = librtk.rtksvropenstr(svr,index,str,path,solopt)


  return result

librtk.rtksvrclosestr.argtypes = [ctypes.POINTER(rtksvr_t),ctypes.c_int32]
librtk.rtksvrclosestr.restype = ctypes.c_void_p
def rtksvrclosestr(svr,index):
  """
rtksvrclosestr(rtksvr_t *svr, int index"""

  result = librtk.rtksvrclosestr(svr,index)


  return result

librtk.rtksvrlock.argtypes = [ctypes.POINTER(rtksvr_t)]
librtk.rtksvrlock.restype = ctypes.c_void_p
def rtksvrlock(svr):
  """
rtksvrlock  (rtksvr_t *svr"""

  result = librtk.rtksvrlock(svr)


  return result

librtk.rtksvrunlock.argtypes = [ctypes.POINTER(rtksvr_t)]
librtk.rtksvrunlock.restype = ctypes.c_void_p
def rtksvrunlock(svr):
  """
rtksvrunlock(rtksvr_t *svr"""

  result = librtk.rtksvrunlock(svr)


  return result

librtk.rtksvrostat.argtypes = [ctypes.POINTER(rtksvr_t),ctypes.c_int32,ctypes.POINTER(gtime_t),ctypes.POINTER(ctypes.c_int32),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_int32),ctypes.POINTER(ctypes.c_int32)]
librtk.rtksvrostat.restype = ctypes.c_int32
def rtksvrostat(svr,type,time,sat,az,el,snr,vsat):
  """
rtksvrostat (rtksvr_t *svr, int type, gtime_t *time, int *sat,
                         double *az, double *el, int **snr, int *vsat"""

  result = librtk.rtksvrostat(svr,type,time,sat,az,el,snr,vsat)


  return result

librtk.rtksvrsstat.argtypes = [ctypes.POINTER(rtksvr_t),ctypes.POINTER(ctypes.c_int32),ctypes.POINTER(ctypes.c_char)]
librtk.rtksvrsstat.restype = ctypes.c_void_p
def rtksvrsstat(svr,sstat,msg):
  """
rtksvrsstat (rtksvr_t *svr, int *sstat, char *msg"""

  result = librtk.rtksvrsstat(svr,sstat,msg)


  return result

librtk.rtksvrmark.argtypes = [ctypes.POINTER(rtksvr_t),ctypes.POINTER(ctypes.c_char),ctypes.POINTER(ctypes.c_char)]
librtk.rtksvrmark.restype = ctypes.c_int32
def rtksvrmark(svr,name,comment):
  """
rtksvrmark(rtksvr_t *svr, const char *name, const char *comment"""

  result = librtk.rtksvrmark(svr,name,comment)


  return result

librtk.dl_readurls.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.POINTER(ctypes.c_char),ctypes.c_int32,ctypes.POINTER(url_t),ctypes.c_int32]
librtk.dl_readurls.restype = ctypes.c_int32
def dl_readurls(file,types,ntype,urls,nmax):
  """
dl_readurls(const char *file, char **types, int ntype, url_t *urls,
                       int nmax"""

  result = librtk.dl_readurls(file,types,ntype,urls,nmax)


  return result

librtk.dl_readstas.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.POINTER(ctypes.c_char),ctypes.c_int32]
librtk.dl_readstas.restype = ctypes.c_int32
def dl_readstas(file,stas,nmax):
  """
dl_readstas(const char *file, char **stas, int nmax"""

  result = librtk.dl_readstas(file,stas,nmax)


  return result

librtk.dl_exec.argtypes = [gtime_t,gtime_t,ctypes.c_double,ctypes.c_int32,ctypes.c_int32,ctypes.POINTER(url_t),ctypes.c_int32,ctypes.POINTER(ctypes.c_char),ctypes.c_int32,ctypes.POINTER(ctypes.c_char),ctypes.POINTER(ctypes.c_char),ctypes.POINTER(ctypes.c_char),ctypes.POINTER(ctypes.c_char),ctypes.c_int32,ctypes.POINTER(ctypes.c_char),ctypes.POINTER(__sFILE)]
librtk.dl_exec.restype = ctypes.c_int32
def dl_exec(ts,te,ti,seqnos,seqnoe,urls,nurl,stas,nsta,dir,usr,pwd,proxy,opts,msg,fp):
  """
dl_exec(gtime_t ts, gtime_t te, double ti, int seqnos, int seqnoe,
                   const url_t *urls, int nurl, char **stas, int nsta,
                   const char *dir, const char *usr, const char *pwd,
                   const char *proxy, int opts, char *msg, FILE *fp"""

  result = librtk.dl_exec(ts,te,ti,seqnos,seqnoe,urls,nurl,stas,nsta,dir,usr,pwd,proxy,opts,msg,fp)


  return result

librtk.dl_test.argtypes = [gtime_t,gtime_t,ctypes.c_double,ctypes.POINTER(url_t),ctypes.c_int32,ctypes.POINTER(ctypes.c_char),ctypes.c_int32,ctypes.POINTER(ctypes.c_char),ctypes.c_int32,ctypes.c_int32,ctypes.POINTER(__sFILE)]
librtk.dl_test.restype = ctypes.c_void_p
def dl_test(ts,te,ti,urls,nurl,stas,nsta,dir,ncol,datefmt,fp):
  """
dl_test(gtime_t ts, gtime_t te, double ti, const url_t *urls,
                    int nurl, char **stas, int nsta, const char *dir,
                    int ncol, int datefmt, FILE *fp"""

  result = librtk.dl_test(ts,te,ti,urls,nurl,stas,nsta,dir,ncol,datefmt,fp)


  return result

librtk.showmsg.argtypes = [ctypes.POINTER(ctypes.c_char)]
librtk.showmsg.restype = ctypes.c_int32
def showmsg(format):
  """
showmsg(const char *format,..."""

  result = librtk.showmsg(format)


  return result

librtk.settspan.argtypes = [gtime_t,gtime_t]
librtk.settspan.restype = ctypes.c_void_p
def settspan(ts,te):
  """
settspan(gtime_t ts, gtime_t te"""

  result = librtk.settspan(ts,te)


  return result

librtk.settime.argtypes = [gtime_t]
librtk.settime.restype = ctypes.c_void_p
def settime(time):
  """
settime(gtime_t time"""

  result = librtk.settime(time)


  return result


