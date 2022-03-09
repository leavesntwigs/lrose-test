#include <limits.h>
#include <math.h>
#include "gtest/gtest.h"
#include "Solo/SoloFunctions.hh"

namespace {

// Step 2. Use the TEST macro to define your tests.
//
// TEST has two parameters: the test case name and the test name.
// After using the macro, you should define your test logic between a
// pair of braces.  You can use a bunch of macros to indicate the
// success or failure of a test.  EXPECT_TRUE and EXPECT_EQ are
// examples of such macros.  For a complete list, see gtest.h.
//
// <TechnicalDetails>
//
// In Google Test, tests are grouped into test cases.  This is how we
// keep test code organized.  You should put logically related tests
// into the same test case.
//
// The test case name and the test name should both be valid C++
// identifiers.  And you should not use underscore (_) in the names.
//
// Google Test guarantees that each test you define is run exactly
// once, but it makes no guarantee on the order the tests are
// executed.  Therefore, you should write your tests in such a way
// that their results don't depend on their order.
//
// </TechnicalDetails>


// Keep the interface simple
// Inside the C++ code, the structures can be more complicated
//

// test variables are:
//  --- amount of change ---| ------  which data are changed -|
// adjust= ac vel | nyquist                          | clip_gate | boundary | bad data |
//                | data folding | aircraft velocity |           |          |          |
//                |              |  folding          |           |          |          |
//                | w/o          | with   | w/o      |          
//                | max vel      | max vel| max vel  |
// ---------------|--------------|-------------------|-----------|----------|----------|
//  

#define NGATES_4 4
#define NGATES_MANY 124
#define MISS -9999999
  TEST(SoloRemoveSurface, cfrad_data) {

    //float data[NGATES_MANY] = {3,4,5,6};
    float newData[NGATES_MANY]; // = {0,0,0,0};
    bool bnd[NGATES_MANY]; // = {1,1,1,1};
    float data[NGATES_MANY] =
{15.670, 15.850, 16.720, 14.930, 15.110, 16.810, 15.620, 
13.990, 15.490, 18.210, 15.480, 17.740, 20.350, 15.950, 
15.040, 14.570, 14.320, 14.010, 13.760, 12.910, -9999999, -9999999,
13.530, -9999999, 15.870, 14.500, 14.820, 14.740, 11.500, 
11.200, 7.760, 2.030, -2.550, -9999999, -8.590, -7.410, 
-5.330, -4.240, -4.710, -4.130, -12.380, -15.300, -14.740, 
-14.760, -9999999, 2.810, 2.030, -0.290, -5.100, -6.620, 
1.740, 0.090, -9999999, -9999999, -9999999, -9999999, -7.090, -2.760, -3.740, -1.170, 
-19.660, -1.560, -4.370, -2.910, -2.660, -1.560, -1.540, 
-0.280, 0.410, -3.200, -9.940, -3.950, 1.190, 0.720, 
-1.500, -1.690, 0.330, 1.140, 2.970, 0.470, 0.510, 
0.400, 0.600, -1.500, 0.370, -1.460, -1.150, 1.000, 
-0.150, -0.640, -3.010, -3.700, -5.840, 0.110, 0.030, 
-1.640, -0.610, -1.130, -1.710, -0.190, -0.510, 0.060, 
-0.770, -1.380, -1.280, -1.430, -1.960, -2.470, -2.470, -1.980, 
-0.450, -0.280, -1.210, -3.120, -2.400, -1.500,-0.870, 
-1.760, -2.250, -2.340, -2.540, 0.300, -0.190, -0.540 
};

    size_t nGates = NGATES_MANY;
    size_t clip_gate = nGates;
    float newData_expected[NGATES_MANY] = 
{ 15.670, 15.850, 16.720, 14.930, 15.110, 16.810, 15.620, 
13.990, 15.490, 18.210, 15.480, 17.740, 20.350, 15.950, 
15.040, 14.570, 14.320, 14.010, 13.760, 12.910, -9999999, -9999999, 
13.530, -9999999, 15.870, 14.500, 14.820, 14.740, 11.500, 
11.200, 7.760, 2.030, -2.550, -9999999, -8.590, -7.410, 
-5.330, -4.240, -4.710, -4.130, -12.380, -15.300, -14.740, 
-14.760, -9999999, 2.810, 2.030, -0.290, -5.100, -6.620, 
1.740, 0.090, -9999999, -9999999, -9999999, -9999999, -7.090, -2.760, -3.740, -1.170, 
-19.660, -1.560, -4.370, -2.910, -2.660, -1.560, -1.540, 
-0.280, 0.410, -3.200, -9.940, -3.950, 1.190, 0.720, 
-1.500, -1.690, 0.330, 1.140, 2.970, 0.470, MISS,
MISS, MISS, MISS, MISS, MISS, MISS, MISS, 
MISS, MISS, MISS, MISS, MISS, MISS, MISS, 
MISS, MISS, MISS, MISS, MISS, MISS, MISS, 
MISS, MISS, MISS, MISS, MISS, MISS, MISS, 
MISS, MISS, MISS, MISS, MISS, MISS, MISS, MISS, 
MISS, MISS, MISS, MISS, MISS, MISS,MISS 
}; 



    /*
from ~/data/from_Alex/radarqc_scans/radarqc_scans-main/airborne_qc/input/cfrad.20181010_122951.196_to_20181010_122955.166_N42RF-TS_AIR.nc

=============== RadxCfactors ===============
Correction factors:
  azimuthCorr: 0
  elevationCorr: 0
  rangeCorr: 0
  longitudeCorr: 0
  latitudeCorr: 0
  pressureAltCorr: 0
  altitudeCorr: 0
  ewVelCorr: 0
  nsVelCorr: 0
  vertVelCorr: 0
  headingCorr: 0
  rollCorr: 0
  pitchCorr: 0
  driftCorr: 0
  rotationCorr: 0
  tiltCorr: 0


=============== RadxRay ===============
  volNum: 3394
  sweepNum: 0
  calibIndex: 0
  sweepMode: elevation_surveillance
  polarizationMode: horizontal
  prtMode: fixed
  followMode: none
  timeSecs: 2018/10/10 12:29:51.549000
  az: 99.6872
  elev: -19.9924
  fixedAngle: -20.0006
  targetScanRate: -9999
  trueScanRate: -9999
  isIndexed: 0
  angleRes: 1
  antennaTransition: 0
  nSamples: 35
  pulseWidthUsec: 13.3025
  prtSec: 0.000320513
  prtRatio: 1
  nyquistMps: 24.96
  unambigRangeKm: 48.0437
  measXmitPowerDbmH: -9999
  measXmitPowerDbmV: -9999
  eventFlagsSet: N
  georefApplied: Y
  nGates: 627
  RadxRangeGeom:
    rangeGeomSet: Y
    startRangeKm: 0
    gateSpacingKm: 0.075
  nFields: 1
    VG:m/s


    Geo-reference variables:
  time: 2018/10/10 12:29:51.549000 UTC
  unitNum: 0
  unitId: 0
  longitude: -86.3242
  latitude: 29.0472
  altitudeKmMsl: 1.9117
  altitudeKmAgl: 1.95904
  ewVelocity: 63.45
  nsVelocity: 107.39
  vertVelocity: -0.81
  heading: 27.9492
  track: -9999
  roll: 8.14636
  pitch: 1.97205
  drift: 2.62573
  rotation: 99.6872
  tilt: -19.9924
  ewWind: 5.09053
  nsWind: -4.84845
  vertWind: -1.42
  headingRate: 0.769043
  pitchRate: -0.170288
  rollRate: -9999
  driveAngle1: -9999
  driveAngle2: -9999

  ================== Data ===================
15.670 15.850 16.720 14.930 15.110 16.810 15.620 
13.990 15.490 18.210 15.480 17.740 20.350 15.950 
15.040 14.570 14.320 14.010 13.760 12.910 2*MISS 
13.530 MISS 15.870 14.500 14.820 14.740 11.500 
11.200 7.760 2.030 -2.550 MISS -8.590 -7.410 
-5.330 -4.240 -4.710 -4.130 -12.380 -15.300 -14.740 
-14.760 MISS 2.810 2.030 -0.290 -5.100 -6.620 
1.740 0.090 4*MISS -7.090 -2.760 -3.740 -1.170 
-19.660 -1.560 -4.370 -2.910 -2.660 -1.560 -1.540 
-0.280 0.410 -3.200 -9.940 -3.950 1.190 0.720 
-1.500 -1.690 0.330 1.140 2.970 0.470 0.510 
0.400 0.600 -1.500 0.370 -1.460 -1.150 1.000 
-0.150 -0.640 -3.010 -3.700 -5.840 0.110 0.030 
-1.640 -0.610 -1.130 -1.710 -0.190 -0.510 0.060 
-0.770 -1.380 -1.280 -1.430 -1.960 2*-2.470 -1.980 
-0.450 -0.280 -1.210 -3.120 -2.400 -1.500 -0.870 
-1.760 -2.250 -2.340 -2.540 0.300 -0.190 -0.540 
0.170 3.040 -1.050 MISS 0.860 3*MISS 1.930 
10*MISS -4.280 2*MISS 9.990 10.670 3*MISS 12.530 
13.880 12.040 10.870 10*MISS -0.030 2*MISS 0.710 
2.240 -0.110 1.010 -2.410 -2.690 0.180 -0.090 
-0.390 -0.520 2.950 1.800 2.600 6.600 8.490 
0.760 -1.450 0.440 0.240 -0.390 0.310 -1.590 
2.140 0.810 1.540 MISS -0.330 1.060 1.170 
1.730 1.320 5*MISS -9.920 2*MISS -0.830 MISS 
...


expected output ..

================== Data ===================
15.670 15.850 16.720 14.930 15.110 16.810 15.620 
13.990 15.490 18.210 15.480 17.740 20.350 15.950 
15.040 14.570 14.320 14.010 13.760 12.910 2*MISS 
13.530 MISS 15.870 14.500 14.820 14.740 11.500 
11.200 7.760 2.030 -2.550 MISS -8.590 -7.410 
-5.330 -4.240 -4.710 -4.130 -12.380 -15.300 -14.740 
-14.760 MISS 2.810 2.030 -0.290 -5.100 -6.620 
1.740 0.090 4*MISS -7.090 -2.760 -3.740 -1.170 
-19.660 -1.560 -4.370 -2.910 -2.660 -1.560 -1.540 
-0.280 0.410 -3.200 -9.940 -3.950 1.190 0.720 
-1.500 -1.690 0.330 1.140 2.970 0.470 547*MISS 
===========================================
  */


/* 
see data file: 
~/data/from_Alex/radarqc_scans/radarqc_scans-main/airborne_qc/RadxConvert_with_cfac/output/20181010/cfrad.20181010_122951.196_to_20181010_122955.166_N42RF-TS_AIR.nc
works with ra_elevation taken from ray at 
=============== RadxRay ===============
  volNum: 3394
  sweepNum: 0
  calibIndex: 0
  sweepMode: elevation_surveillance
  polarizationMode: horizontal
  prtMode: fixed
  followMode: none
  timeSecs: 2018/10/10 12:29:51.549000
  az: 137.549
  elev: -17.4617

which corresponds to the ray at az: 99.286 
before applying cfac.aft
*/

  float ra_elevation = -17.4617 * M_PI / 180.0; 
  printf("ra_elevation (radians) = %f\n", ra_elevation);

    Surface_Type which_removal = ONLY_SURFACE;  // internal value based on function call
       float optimal_beamwidth = 3;      // script parameter; origin seds->optimal_beamwidth
       int seds_surface_gate_shift = 0;       // script parameter; origin seds->surface_gate_shift
       float vert_beam_width = 2; // radarBeamWidthDegV:         // from radar angles???; origin dgi->dds->radd->vert_beam_width
// =============== DoradeData platform ===============
//  id: ASIB
//  nbytes: 80
//  sizeof(platform_t): 80
//  longitude: -86.3244
//  latitude: 29.0469
//  altitude_msl: 1.91292
//  altitude_agl: 1.95904
// from https://www.eol.ucar.edu/node/1883   
//Antenna Altitude above ground level (AGL) in m
// DORADE has altitude_agl in meters, but cfrad/RadxVol has altitudeKmAgl in Km       
       float asib_altitude_agl = 1.95904;  // altitudeKmAgl: 1.95904  // altitude angle (gets multiplied by 1000; so in km?)
       float dds_ra_elevation = -17.4617 * M_PI / 180.0;       // radar angles!! requires cfac values and calculation
                                     // origin dds->ra->elevation, ra = radar_angles
                                     // get this from RadxRay::_elev if RadxRay::_georefApplied == true
       bool getenv_ALTERNATE_GECHO = false;  // script parameter
       double d = 0.0; // used for min_grad, if getenv_ALTERNATE_GECHO is true
       // d = ALTERNATE_GECHO environment variable
       double dds_asib_rotation_angle = 99.6872;  // origin dds->asib->rotation_angle;  asib is struct platform_i
       double dds_asib_roll = 8.14636;            // origin dds->asib->roll
       double dds_cfac_rot_angle_corr = 0.0;  // origin dds->cfac->rot_angle_corr; cfac is struct correction_d
       float radar_latitude = 29.0469;  // radar->latitude 
       //const float *data;     // internal value
       float *new_data = newData;       // internal value
       //size_t nGates;         // internal value
       float gate_size = 0.075;  // gateSpacingKm
       float distance_to_first_gate = 0.0;  // startRangeKm
       // TODO: should be nGates, but we are using a test number of gates
       double max_range_in_km = distance_to_first_gate + gate_size * NGATES_MANY;      // internal value; origin dds->celvc_dist_cells[dgi_clip_gate];
       float bad_data_value = -9999999;  // default value
       size_t dgi_clip_gate = clip_gate;  // default value
       bool *boundary_mask = bnd;

    se_ac_surface_tweak(which_removal, optimal_beamwidth, seds_surface_gate_shift,
       vert_beam_width, asib_altitude_agl, dds_ra_elevation, getenv_ALTERNATE_GECHO, d,
       dds_asib_rotation_angle, dds_asib_roll, dds_cfac_rot_angle_corr, radar_latitude,
       data, new_data, nGates, gate_size, distance_to_first_gate, max_range_in_km,
       bad_data_value, dgi_clip_gate, boundary_mask
      );


    //(vert_velocity, ew_velocity, ns_velocity,
		//	ew_gndspd_corr, tilt, elevation,
		//	data, newData, nGates, bad_flag, clip_gate,
		//	eff_unamb_vel, nyquist_velocity, bnd);
    for (int i=0; i<NGATES_MANY; i++)
      EXPECT_EQ(newData[i], newData_expected[i]);
    
  }



TEST(SoloRemoveSurface, original_dorade_data) {

    //float data[NGATES_MANY] = {3,4,5,6};
    float newData[NGATES_MANY]; // = {0,0,0,0};
    bool bnd[NGATES_MANY]; // = {1,1,1,1};
    float data[NGATES_MANY] =
{15.670, 15.850, 16.720, 14.930, 15.110, 16.810, 15.620, 
13.990, 15.490, 18.210, 15.480, 17.740, 20.350, 15.950, 
15.040, 14.570, 14.320, 14.010, 13.760, 12.910, -9999999, -9999999,
13.530, -9999999, 15.870, 14.500, 14.820, 14.740, 11.500, 
11.200, 7.760, 2.030, -2.550, -9999999, -8.590, -7.410, 
-5.330, -4.240, -4.710, -4.130, -12.380, -15.300, -14.740, 
-14.760, -9999999, 2.810, 2.030, -0.290, -5.100, -6.620, 
1.740, 0.090, -9999999, -9999999, -9999999, -9999999, -7.090, -2.760, -3.740, -1.170, 
-19.660, -1.560, -4.370, -2.910, -2.660, -1.560, -1.540, 
-0.280, 0.410, -3.200, -9.940, -3.950, 1.190, 0.720, 
-1.500, -1.690, 0.330, 1.140, 2.970, 0.470, 0.510, 
0.400, 0.600, -1.500, 0.370, -1.460, -1.150, 1.000, 
-0.150, -0.640, -3.010, -3.700, -5.840, 0.110, 0.030, 
-1.640, -0.610, -1.130, -1.710, -0.190, -0.510, 0.060, 
-0.770, -1.380, -1.280, -1.430, -1.960, -2.470, -2.470, -1.980, 
-0.450, -0.280, -1.210, -3.120, -2.400, -1.500,-0.870, 
-1.760, -2.250, -2.340, -2.540, 0.300, -0.190, -0.540 
};

    size_t nGates = NGATES_MANY;
    size_t clip_gate = nGates;
    float newData_expected[NGATES_MANY] = 
{ 15.670, 15.850, 16.720, 14.930, 15.110, 16.810, 15.620, 
13.990, 15.490, 18.210, 15.480, 17.740, 20.350, 15.950, 
15.040, 14.570, 14.320, 14.010, 13.760, 12.910, -9999999, -9999999, 
13.530, -9999999, 15.870, 14.500, 14.820, 14.740, 11.500, 
11.200, 7.760, 2.030, -2.550, -9999999, -8.590, -7.410, 
-5.330, -4.240, -4.710, -4.130, -12.380, -15.300, -14.740, 
-14.760, -9999999, 2.810, 2.030, -0.290, -5.100, -6.620, 
1.740, 0.090, -9999999, -9999999, -9999999, -9999999, -7.090, -2.760, -3.740, -1.170, 
-19.660, -1.560, -4.370, -2.910, -2.660, -1.560, -1.540, 
-0.280, 0.410, -3.200, -9.940, -3.950, 1.190, 0.720, 
-1.500, -1.690, 0.330, 1.140, 2.970, 0.470, MISS,
MISS, MISS, MISS, MISS, MISS, MISS, MISS, 
MISS, MISS, MISS, MISS, MISS, MISS, MISS, 
MISS, MISS, MISS, MISS, MISS, MISS, MISS, 
MISS, MISS, MISS, MISS, MISS, MISS, MISS, 
MISS, MISS, MISS, MISS, MISS, MISS, MISS, MISS, 
MISS, MISS, MISS, MISS, MISS, MISS,MISS 
}; 



    /*
from ~/data/from_Alex/radarqc_scans/radarqc_scans-main/airborne_qc/input/cfrad.20181010_122951.196_to_20181010_122955.166_N42RF-TS_AIR.nc

=============== RadxCfactors ===============
Correction factors:
  azimuthCorr: 0
  elevationCorr: 0
  rangeCorr: 0
  longitudeCorr: 0
  latitudeCorr: 0
  pressureAltCorr: 0
  altitudeCorr: 0
  ewVelCorr: 0
  nsVelCorr: 0
  vertVelCorr: 0
  headingCorr: 0
  rollCorr: 0
  pitchCorr: 0
  driftCorr: 0
  rotationCorr: 0
  tiltCorr: 0


=============== RadxRay ===============
  volNum: 3394
  sweepNum: 0
  calibIndex: 0
  sweepMode: elevation_surveillance
  polarizationMode: horizontal
  prtMode: fixed
  followMode: none
  timeSecs: 2018/10/10 12:29:51.549000
  az: 99.6872
  elev: -19.9924
  fixedAngle: -20.0006
  targetScanRate: -9999
  trueScanRate: -9999
  isIndexed: 0
  angleRes: 1
  antennaTransition: 0
  nSamples: 35
  pulseWidthUsec: 13.3025
  prtSec: 0.000320513
  prtRatio: 1
  nyquistMps: 24.96
  unambigRangeKm: 48.0437
  measXmitPowerDbmH: -9999
  measXmitPowerDbmV: -9999
  eventFlagsSet: N
  georefApplied: Y
  nGates: 627
  RadxRangeGeom:
    rangeGeomSet: Y
    startRangeKm: 0
    gateSpacingKm: 0.075
  nFields: 1
    VG:m/s


    Geo-reference variables:
  time: 2018/10/10 12:29:51.549000 UTC
  unitNum: 0
  unitId: 0
  longitude: -86.3242
  latitude: 29.0472
  altitudeKmMsl: 1.9117
  altitudeKmAgl: 1.95904
  ewVelocity: 63.45
  nsVelocity: 107.39
  vertVelocity: -0.81
  heading: 27.9492
  track: -9999
  roll: 8.14636
  pitch: 1.97205
  drift: 2.62573
  rotation: 99.6872
  tilt: -19.9924
  ewWind: 5.09053
  nsWind: -4.84845
  vertWind: -1.42
  headingRate: 0.769043
  pitchRate: -0.170288
  rollRate: -9999
  driveAngle1: -9999
  driveAngle2: -9999

  cfac.aft
eol-albireo:cfac brenda$ more cfac.aft
azimuth_corr           =   0.000
elevation_corr         =   0.000
range_delay_corr       = -16.641
longitude_corr         =   0.000
latitude_corr          =   0.000
pressure_alt_corr      =   4.969
radar_alt_corr         =   0.000
ew_gndspd_corr         =   0.000
ns_gndspd_corr         =   0.000
vert_vel_corr          =   0.000
heading_corr           =   0.000
roll_corr              =   0.000
pitch_corr             =   0.009
drift_corr             =   0.119
rot_angle_corr         =  -0.016
tilt_corr              =   0.713

  ---- from DORADE swp file: input/swp.1181010122951.N42RF-TS.196.-20.0_AIR_v3394
  eol-albireo:input brenda$ ~/lrose/bin/RadxPrint -native  -f swp.1181010122951.N42RF-TS.196.-20.0_AIR_v3394  -field VG -rays -data | less


  radar_type: RADAR_AIR_TAIL

  id: CFAC
  nbytes: 72
  sizeof(correction_t): 72
  azimuth_corr: 0
  elevation_corr: 0
  range_delay_corr: 0
  longitude_corr: 0
  latitude_corr: 0
  pressure_alt_corr: 0
  radar_alt_corr: 0
  ew_gndspd_corr: 0
  ns_gndspd_corr: 0
  vert_vel_corr: 0
  heading_corr: 0
  roll_corr: 0
  pitch_corr: 0
  drift_corr: 0
  rot_angle_corr: 0
  tilt_corr: 0
=================

=============== DoradeData ray ===============
  id: RYIB
  nbytes: 44
  sizeof(ray_t): 44
  sweep_num: 0
  julian_day: 283
  hour: 12
  minute: 29
  second: 51
  millisecond: 549
  azimuth: 99.6872
  elevation: -19.9924
  peak_power: -999
  true_scan_rate: -9999
  ray_status: 0
==============================================
=============== DoradeData platform ===============
  id: ASIB
  nbytes: 80
  sizeof(platform_t): 80
  longitude: -86.3242
  latitude: 29.0472
  altitude_msl: 1.9117
  altitude_agl: 1.95904
  ew_velocity: 63.45
  ns_velocity: 107.39
  vert_velocity: -0.81
  heading: 27.9492
  roll: 8.14636
  pitch: 1.97205
  drift_angle: 2.62573
  rotation_angle: 99.6872
  tilt: -19.9924
  ew_horiz_wind: 5.09053
  ns_horiz_wind: -4.84845
  vert_wind: -1.42
  heading_change: 0.769043
  pitch_change: -0.170288
===================================================
=============== DoradeData paramdata ===============  

  ================== Data ===================
15.670 15.850 16.720 14.930 15.110 16.810 15.620 
13.990 15.490 18.210 15.480 17.740 20.350 15.950 
15.040 14.570 14.320 14.010 13.760 12.910 2*MISS 
13.530 MISS 15.870 14.500 14.820 14.740 11.500 
11.200 7.760 2.030 -2.550 MISS -8.590 -7.410 
-5.330 -4.240 -4.710 -4.130 -12.380 -15.300 -14.740 
-14.760 MISS 2.810 2.030 -0.290 -5.100 -6.620 
1.740 0.090 4*MISS -7.090 -2.760 -3.740 -1.170 
-19.660 -1.560 -4.370 -2.910 -2.660 -1.560 -1.540 
-0.280 0.410 -3.200 -9.940 -3.950 1.190 0.720 
-1.500 -1.690 0.330 1.140 2.970 0.470 0.510 
0.400 0.600 -1.500 0.370 -1.460 -1.150 1.000 
-0.150 -0.640 -3.010 -3.700 -5.840 0.110 0.030 
-1.640 -0.610 -1.130 -1.710 -0.190 -0.510 0.060 
-0.770 -1.380 -1.280 -1.430 -1.960 2*-2.470 -1.980 
-0.450 -0.280 -1.210 -3.120 -2.400 -1.500 -0.870 
-1.760 -2.250 -2.340 -2.540 0.300 -0.190 -0.540 
0.170 3.040 -1.050 MISS 0.860 3*MISS 1.930 
10*MISS -4.280 2*MISS 9.990 10.670 3*MISS 12.530 
13.880 12.040 10.870 10*MISS -0.030 2*MISS 0.710 
2.240 -0.110 1.010 -2.410 -2.690 0.180 -0.090 
-0.390 -0.520 2.950 1.800 2.600 6.600 8.490 
0.760 -1.450 0.440 0.240 -0.390 0.310 -1.590 
2.140 0.810 1.540 MISS -0.330 1.060 1.170 
1.730 1.320 5*MISS -9.920 2*MISS -0.830 MISS 
...


expected output ..

================== Data ===================
15.670 15.850 16.720 14.930 15.110 16.810 15.620 
13.990 15.490 18.210 15.480 17.740 20.350 15.950 
15.040 14.570 14.320 14.010 13.760 12.910 2*MISS 
13.530 MISS 15.870 14.500 14.820 14.740 11.500 
11.200 7.760 2.030 -2.550 MISS -8.590 -7.410 
-5.330 -4.240 -4.710 -4.130 -12.380 -15.300 -14.740 
-14.760 MISS 2.810 2.030 -0.290 -5.100 -6.620 
1.740 0.090 4*MISS -7.090 -2.760 -3.740 -1.170 
-19.660 -1.560 -4.370 -2.910 -2.660 -1.560 -1.540 
-0.280 0.410 -3.200 -9.940 -3.950 1.190 0.720 
-1.500 -1.690 0.330 1.140 2.970 0.470 547*MISS 
===========================================
  */

     float asib_roll = 8.14636;
     float asib_pitch = 1.97205;
     float asib_heading = 27.9492;
     float asib_drift_angle = 2.62573;
     float asib_rotation_angle = 99.6872;
     float asib_tilt = -19.9924;

/* from cfac.aft file
azimuth_corr           =   0.000
elevation_corr         =   0.000
range_delay_corr       = -16.641
longitude_corr         =   0.000
latitude_corr          =   0.000
pressure_alt_corr      =   4.969
radar_alt_corr         =   0.000
ew_gndspd_corr         =   0.000
ns_gndspd_corr         =   0.000
vert_vel_corr          =   0.000
heading_corr           =   0.000
roll_corr              =   0.000
pitch_corr             =   0.009
drift_corr             =   0.119
rot_angle_corr         =  -0.016
tilt_corr              =   0.713
*/


     float cfac_pitch_corr =   0.009;
     float cfac_heading_corr = 0.0;
     float cfac_drift_corr =   0.119;
     float cfac_roll_corr = 0.0; 
     float cfac_elevation_corr = 0.0;
     float cfac_azimuth_corr = 0.0;
     float cfac_rot_angle_corr =  -0.016;
     float cfac_tilt_corr =   0.713;
     int radar_type = 3;  // from dgi->dds->radd->radar_type  RADAR_AIR_TAIL
      // # define         AIR_TAIL 3
     bool use_Wen_Chaus_algorithm = true;

    float dgi_dds_ryib_azimuth = 99.6872;
    float dgi_dds_ryib_elevation = -19.9924;
     float ra_x;
     float ra_y;
     float ra_z;
     float ra_rotation_angle;
     float ra_tilt;
     float ra_azimuth;
     float ra_elevation;
     float ra_psi;

   dd_radar_angles( 
      asib_roll,
      asib_pitch,
      asib_heading,
      asib_drift_angle,
      asib_rotation_angle,
      asib_tilt,
      cfac_pitch_corr,
      cfac_heading_corr,
      cfac_drift_corr,
      cfac_roll_corr,
      cfac_elevation_corr,
      cfac_azimuth_corr,
      cfac_rot_angle_corr,
      cfac_tilt_corr,
      radar_type,  // from dgi->dds->radd->radar_type
      use_Wen_Chaus_algorithm,
     dgi_dds_ryib_azimuth,
     dgi_dds_ryib_elevation,
      &ra_x,
      &ra_y,
      &ra_z,
      &ra_rotation_angle,
      &ra_tilt,
      &ra_azimuth,
      &ra_elevation,
      &ra_psi
     );


    printf("ra_elevation (radians) = %f\n", ra_elevation);

    Surface_Type which_removal = ONLY_SURFACE;  // internal value based on function call
       float optimal_beamwidth = 3;      // script parameter; origin seds->optimal_beamwidth
       int seds_surface_gate_shift = 0;       // script parameter; origin seds->surface_gate_shift
       float vert_beam_width = 2; // radarBeamWidthDegV:         // from radar angles???; origin dgi->dds->radd->vert_beam_width
// =============== DoradeData platform ===============
//  id: ASIB
//  nbytes: 80
//  sizeof(platform_t): 80
//  longitude: -86.3244
//  latitude: 29.0469
//  altitude_msl: 1.91292
//  altitude_agl: 1.95904
// from https://www.eol.ucar.edu/node/1883   
//Antenna Altitude above ground level (AGL) in m
// DORADE has altitude_agl in meters, but cfrad/RadxVol has altitudeKmAgl in Km    

       float asib_altitude_agl = 1.95904;  // agrees // altitudeKmAgl: 1.95904  // altitude angle (gets multiplied by 1000; so in km?)
       float dds_ra_elevation = ra_elevation; // IN RADIANS!! // -19.9924;   // changed by navigation corrections  
         // TODO: what is this value???
         // radar angles!! requires cfac values and calculation
                                     // origin dds->ra->elevation, ra = radar_angles
                                     // get this from RadxRay::_elev if RadxRay::_georefApplied == true
       bool getenv_ALTERNATE_GECHO = false;  // script parameter
       double d = 0.0; // used for min_grad, if getenv_ALTERNATE_GECHO is true
       // d = ALTERNATE_GECHO environment variable
       double dds_asib_rotation_angle = 99.6872;  // agrees // origin dds->asib->rotation_angle;  asib is struct platform_i
       double dds_asib_roll = 8.14636;    // agrees         // origin dds->asib->roll
       double dds_cfac_rot_angle_corr =  -0.016;  // origin dds->cfac->rot_angle_corr; cfac is struct correction_d
       float radar_latitude = 29.0472; // differs 29.0469;  // radar->latitude 
       //const float *data;     // internal value
       float *new_data = newData;       // internal value
       //size_t nGates;         // internal value
       float gate_size = 0.075;  // same // gateSpacingKm
       float distance_to_first_gate = 0.0;  // same // startRangeKm
       // TODO: should be nGates, but we are using a test number of gates

       //   eff_unamb_range: 48.0437 ???
       double max_range_in_km = distance_to_first_gate + gate_size * NGATES_MANY;      // internal value; origin dds->celvc_dist_cells[dgi_clip_gate];
       float bad_data_value = -9999999;  // default value
       size_t dgi_clip_gate = clip_gate;  // default value
       bool *boundary_mask = bnd;

    se_ac_surface_tweak(which_removal, optimal_beamwidth, seds_surface_gate_shift,
       vert_beam_width, asib_altitude_agl, dds_ra_elevation, getenv_ALTERNATE_GECHO, d,
       dds_asib_rotation_angle, dds_asib_roll, dds_cfac_rot_angle_corr, radar_latitude,
       data, new_data, nGates, gate_size, distance_to_first_gate, max_range_in_km,
       bad_data_value, dgi_clip_gate, boundary_mask
      );


    //(vert_velocity, ew_velocity, ns_velocity,
    //  ew_gndspd_corr, tilt, elevation,
    //  data, newData, nGates, bad_flag, clip_gate,
    //  eff_unamb_vel, nyquist_velocity, bnd);
    for (int i=0; i<NGATES_MANY; i++)
      EXPECT_EQ(newData[i], newData_expected[i]);
    
  }  
/*
  TEST(SoloRemoveSurface, no_adjust__unfold__no_clipping__no_bad_flags__no_boundary) {

    float data[NGATES_4] = {3,4,-5,6};
    float newData[NGATES_4] = {0,0,0,0};
    bool bnd[NGATES_4] = {1,1,1,1};
    float bad_flag = -3;
    float vert_velocity = 1;
    float ew_velocity = 1;
    float ns_velocity = 1;
    float ew_gndspd_corr = 1;
    float elevation = 0.0; // or any multiple of pi help make ac_vel = 0
    float tilt = 0.0; // or any multiple of pi help make ac_vel = 0
    // ac_vel should be zero

    // Nyquist stuff ...
    // the Nyquist velocity is less than some data values, 
    // should see unfolding
    float eff_unamb_vel = 0.0; // TODO: this comes from data file?
    float nyquist_velocity = 3.2; 

    size_t nGates = NGATES_4;
    size_t clip_gate = nGates;
    float newData_expected[NGATES_4] = {3, -2, 1, 0};

    se_remove_ac_motion(vert_velocity, ew_velocity, ns_velocity,
			ew_gndspd_corr, tilt, elevation,
			data, newData, nGates, bad_flag, clip_gate,
			eff_unamb_vel, nyquist_velocity, bnd);
    for (int i=0; i<NGATES_4; i++)
      EXPECT_EQ(newData[i], newData_expected[i]);
    
  }
  
 
  TEST(SoloRemoveSurface, adjust__no_folding__clip_gate__bad_flags__no_boundary) {

    float data[NGATES_4] =    {-3,6,5,-3};
    float newData[NGATES_4] = { 0,0,0, 0};
    bool bnd[NGATES_4] = {1,1,1,1};
    float bad_flag = -3;

    float vert_velocity = 3; // goes with sin(elevation)
    float ew_velocity = 1;   // these three go with sin(tilt)
    float ns_velocity = 1;
    float ew_gndspd_corr = 1;
    float elevation = M_PI/2.0; // or any multiple of pi help make ac_vel = 0
    float tilt = 0.0; // or any multiple of pi help make ac_vel = 0

    // Nyquist stuff ...
    // keep the Nyquist velocity greater than any data value, 
    // to avoid any folding/unfolding
    float eff_unamb_vel = 0.0; 
    float nyquist_velocity = 10.0;

    size_t nGates = NGATES_4;
    size_t clip_gate = 2;
    float newData_expected[NGATES_4] = {-3,9,5,-3};  // no changed 

    se_remove_ac_motion(vert_velocity, ew_velocity, ns_velocity,
                        ew_gndspd_corr, tilt, elevation,
                        data, newData, nGates, bad_flag, clip_gate,
                        eff_unamb_vel, nyquist_velocity, bnd);

    for (int i=0; i<NGATES_4; i++)
      EXPECT_EQ(newData[i], newData_expected[i]);
  }

  TEST(SoloRemoveSurface, adjust__folding_clip_gate__bad_flags__no_boundary) {

    float data[NGATES_4] = {-3,6,5,-3};
    float newData[NGATES_4] = {0,0,0,0};
    bool bnd[NGATES_4] = {1,1,1,1};
    float bad_flag = -3;

    float vert_velocity = 3;
    float ew_velocity = 1;
    float ns_velocity = 1;
    float ew_gndspd_corr = 1;
    float elevation = M_PI/2.0; // or any multiple of pi help make ac_vel = 0
    float tilt = 0.0; // or any multiple of pi help make ac_vel = 0

    // Nyquist stuff ...
    // keep the Nyquist velocity greater than any data value, 
    // to avoid any folding/unfolding
    float eff_unamb_vel = 0.0; 
    float nyquist_velocity = 5.0; // causes folding

    size_t nGates = NGATES_4;
    size_t clip_gate = 2;
    float newData_expected[NGATES_4] = {-3,-1,5,-3};  // no changed 

    se_remove_ac_motion(vert_velocity, ew_velocity, ns_velocity,
                        ew_gndspd_corr, tilt, elevation,
                        data, newData, nGates, bad_flag, clip_gate,
                        eff_unamb_vel, nyquist_velocity, bnd);

    for (int i=0; i<NGATES_4; i++)
      EXPECT_EQ(newData[i], newData_expected[i]);
  }
  
  TEST(SoloRemoveSurface, ac_vel_folded__clip_gate__no_boundary) {

    float data[NGATES_4] = {-4,-3, 5, 8};
    float newData[NGATES_4] = {0,0,0,0};
    bool bnd[NGATES_4] = {1,1,1,1};
    float bad_flag = -3;

    float vert_velocity = 3;
    float ew_velocity = 10.0;
    float ns_velocity = 0.0;
    float ew_gndspd_corr = 1;  // ac_vel should be 11.0
    float tilt = M_PI/2.0; // or any multiple of pi help make ac_vel = 0
    float elevation = 0.0; // or any multiple of pi help make ac_vel = 0
    // ac_vel should be unfolded to -1.0

    // Nyquist stuff ...
    // keep the Nyquist velocity greater than any data value, 
    // to avoid any folding/unfolding
    float eff_unamb_vel = 0.0; 
    float nyquist_velocity = 6.0; // causes folding

    size_t nGates = NGATES_4;
    size_t clip_gate = 3;
    float newData_expected[NGATES_4] = {-5,-3,4,8};  // no change 

    se_remove_ac_motion(vert_velocity, ew_velocity, ns_velocity,
                        ew_gndspd_corr, tilt, elevation,
                        data, newData, nGates, bad_flag, clip_gate,
                        eff_unamb_vel, nyquist_velocity, bnd);

    for (int i=0; i<NGATES_4; i++)
      EXPECT_EQ(newData[i], newData_expected[i]);
  }

  TEST(SoloRemoveSurface, ac_vel_folded__with_max_vel_instead_of_nyquist__clip_gate__no_boundary) {

    float data[NGATES_4] = {-4,-3, 5, 8};
    float newData[NGATES_4] = {0,0,0,0};
    bool bnd[NGATES_4] = {1,1,1,1};
    float bad_flag = -3;

    float vert_velocity = 3;
    float ew_velocity = 10.0;
    float ns_velocity = 0.0;
    float ew_gndspd_corr = 1;  // ac_vel should be 11.0
    float tilt = M_PI/2.0; // or any multiple of pi help make ac_vel = 0
    float elevation = 0.0; // or any multiple of pi help make ac_vel = 0
    // ac_vel should be unfolded to -1.0

    // Nyquist stuff ...
    // keep the Nyquist velocity greater than any data value, 
    // to avoid any folding/unfolding
    float eff_unamb_vel = 6.0;  // causes folding
    float nyquist_velocity = 0.0; 

    size_t nGates = NGATES_4;
    size_t clip_gate = 3;
    float newData_expected[NGATES_4] = {-5,-3,4,8};  // no change 

    se_remove_ac_motion(vert_velocity, ew_velocity, ns_velocity,
                        ew_gndspd_corr, tilt, elevation,
                        data, newData, nGates, bad_flag, clip_gate,
                        eff_unamb_vel, nyquist_velocity, bnd);

    for (int i=0; i<NGATES_4; i++)
      EXPECT_EQ(newData[i], newData_expected[i]);
  }

  // Boundary tests ...

  // *  TEST(SoloRemoveSurface, no_adjust__unfold__no_clipping__no_bad_flags__boundary) 
  // *   TEST(SoloRemoveSurface, adjust__no_folding__clip_gate__bad_flags__boundary) 
  // *     TEST(SoloRemoveSurface, adjust__folding_clip_gate__bad_flags__boundary) 
  // *	TEST(SoloRemoveSurface, ac_vel_folded__clip_gate__boundary) 
  //   *  TEST(SoloRemoveSurface, ac_vel_folded__with_max_vel_instead_of_nyquist__clip_gate__boundary)

  // *  TEST( ... remove_multifolded_ac_vel_remove_single_folded_velocity NOTE:  shortcoming of remove aircraft vel
  

  TEST(SoloRemoveSurface, no_adjust__unfold__no_clipping__no_bad_flags__boundary) {

#define NGATES_7 7

    float data[NGATES_7] =    {3,-3, 5,-16, 7,-3 ,6};
    float newData[NGATES_7] = {0, 0, 0,  0, 0, 0, 0};
    bool bnd[NGATES_7] =      {0, 0, 1,  1, 0, 1, 1};
    float bad_flag = -3;

    float vert_velocity = 1;
    float ew_velocity = 1;
    float ns_velocity = 1;
    float ew_gndspd_corr = 1;
    float elevation = 0.0; // or any multiple of pi help make ac_vel = 0                                              
    float tilt = 0.0; // or any multiple of pi help make ac_vel = 0                                                   
    // ac_vel should be zero                                                                                          

    // Nyquist stuff ...                                                                                              
    // the Nyquist velocity is less than some data values,                                                            
    // should see unfolding                                                                                           
    float eff_unamb_vel = 0.0; // TODO: this comes from data file?                                                    
    float nyquist_velocity = 3.2;

    size_t nGates = NGATES_7;
    size_t clip_gate = nGates;
    float newData_expected[NGATES_7] = {3,-3,-1,-10, 7,-3, 0};  // single unfolding only!

    se_remove_ac_motion(vert_velocity, ew_velocity, ns_velocity,
                        ew_gndspd_corr, tilt, elevation,
                        data, newData, nGates, bad_flag, clip_gate,
                        eff_unamb_vel, nyquist_velocity, bnd);

    for (int i=0; i<NGATES_7; i++)
      EXPECT_EQ(newData[i], newData_expected[i]);
  }


  TEST(SoloRemoveSurface, adjust__no_folding__clip_gate__bad_flags__boundary) {
#define NGATES_10 10

    float data[NGATES_10] =                { 3,-3, -3, 5, 5,-2, -3, 5, 5, -3};
    float newData[NGATES_10] =             { 0, 0,  0, 0, 0, 0,  0, 0, 0,  0};
    float newData_expected[NGATES_10] =    { 6,-3, -3, 8, 5, 1, -3, 8, 5, -3}; 
    bool  bnd[NGATES_10] =                 { 1, 0,  1, 1, 0, 1,  1, 1, 1,  0};
    float bad_flag = -3;

    float vert_velocity = 3; // goes with sin(elevation)
    float ew_velocity = 1;   // these three go with sin(tilt)
    float ns_velocity = 1;
    float ew_gndspd_corr = 1;
    float elevation = M_PI/2.0; // or any multiple of pi help make ac_vel = 0
    float tilt = 0.0; // or any multiple of pi help make ac_vel = 0 
    // adjust should be 3.0

    // Nyquist stuff ...     
    // keep the Nyquist velocity greater than any data value,
    // to avoid any folding/unfolding 
    float eff_unamb_vel = 0.0;
    float nyquist_velocity = 10.0;

    size_t nGates = NGATES_10;
    size_t clip_gate = 8;

    se_remove_ac_motion(vert_velocity, ew_velocity, ns_velocity,
                        ew_gndspd_corr, tilt, elevation,
                        data, newData, nGates, bad_flag, clip_gate,
                        eff_unamb_vel, nyquist_velocity, bnd);

    for (int i=0; i<NGATES_10; i++)
      EXPECT_EQ(newData[i], newData_expected[i]);
  }


  
  TEST(SoloRemoveSurface, adjust__folding__no_clip_gate__bad_flags__boundary) {

    float data[NGATES_10] =             { 3,-3,  4,-8, 6, 5, -3, 5, 5, -3};
    float newData[NGATES_10] =          { 0, 0,  0, 0, 0, 0,  0, 0, 0,  0};
    // add ac_vel = 3 to each             6, x,    -5, 9,        8, 8,  x
    // then unfold by nyqi = 6            0  x      1, 3,        2, 2,  x
    float newData_expected[NGATES_10] = { 0,-3,  4, 1, 3, 5, -3, 2, 2, -3};
    bool  bnd[NGATES_10] =              { 1, 1,  0, 1, 1, 0,  0, 1, 1,  1};
    float bad_flag = -3;

    float vert_velocity = 3; // goes with sin(elevation)
    float ew_velocity = 1;   // these three go with sin(tilt)
    float ns_velocity = 1;
    float ew_gndspd_corr = 1;
    float elevation = M_PI/2.0; // or any multiple of pi help make ac_vel = 0 
    float tilt = 0.0; // or any multiple of pi help make ac_vel = 0  
    // adjust should be 3 

    // Nyquist stuff ...    
    // keep the Nyquist velocity greater than any data value,
    // to avoid any folding/unfolding 
    float eff_unamb_vel = 0.0;
    float nyquist_velocity = 3.0;

    int nGates = NGATES_10;
    int clip_gate = nGates;

    se_remove_ac_motion(vert_velocity, ew_velocity, ns_velocity,
                        ew_gndspd_corr, tilt, elevation,
                        data, newData, nGates, bad_flag, clip_gate,
                        eff_unamb_vel, nyquist_velocity, bnd);

    for (int i=0; i<NGATES_10; i++)
      EXPECT_EQ(newData[i], newData_expected[i]);
  }

  
  TEST(SoloRemoveSurface, ac_vel_folded__clip_gate__boundary) {

    float data[NGATES_10] =             {-3,-3, -3, 5,-5, 5, -3, 5, 5, -3};
    float newData[NGATES_10] =          { 0, 0,  0, 0, 0, 0,  0, 0, 0,  0};
    //   add adjust                              x,12, 2
    //   unfold                                  x,-8, 2
    float newData_expected[NGATES_10] = {-3,-3, -3,-8, 2, 5, -3, 5, 5, -3};
    bool  bnd[NGATES_10] =              { 0, 0,  1, 1, 1, 0,  0, 0, 0,  0};

    float bad_flag = -3;

    float vert_velocity = 33.67; // goes with sin(elevation)
    float ew_velocity = 1;   // these three go with sin(tilt)
    float ns_velocity = 1;
    float ew_gndspd_corr = 1;
    float elevation = - M_PI/2.0; // or any multiple of pi help make ac_vel = 0 
    float tilt = 0.0; // or any multiple of pi help make ac_vel = 0  
    // adjust should be 7.0 

    // Nyquist stuff ...    
    // keep the Nyquist velocity greater than any data value,
    // to avoid any folding/unfolding 
    float eff_unamb_vel = 0.0;
    float nyquist_velocity = 10.0;

    size_t nGates = NGATES_10;
    size_t clip_gate = 8;

    se_remove_ac_motion(vert_velocity, ew_velocity, ns_velocity,
                        ew_gndspd_corr, tilt, elevation,
                        data, newData, nGates, bad_flag, clip_gate,
                        eff_unamb_vel, nyquist_velocity, bnd);

    for (int i=0; i<NGATES_10; i++)
      EXPECT_EQ(newData[i], newData_expected[i]);
   }
  
  TEST(SoloRemoveSurface, ac_vel_folded__with_max_vel_instead_of_nyquist__clip_gate__boundary) {
 
    float data[NGATES_10] =             {-3,-3, -3, 5,-5, 5, -3, 5, 5,  5};
    float newData[NGATES_10] =          { 0, 0,  0, 0, 0, 0,  0, 0, 0,  0};
    //   add adjust                              x,12, 2           12
    //   unfold                                  x,-8, 2           -8
    float newData_expected[NGATES_10] = {-3,-3, -3,-8, 2, 5, -3, 5,-8,  5};
    bool  bnd[NGATES_10] =              { 0, 0,  1, 1, 1, 0,  0, 0, 1,  1};

    float bad_flag = -3;

    float vert_velocity = 33.67; // goes with sin(elevation)
    float ew_velocity = 1;   // these three go with sin(tilt)
    float ns_velocity = 1;
    float ew_gndspd_corr = 1;
    float elevation = - M_PI/2.0; // or any multiple of pi help make ac_vel = 0 
    float tilt = 0.0; // or any multiple of pi help make ac_vel = 0  
    // adjust should be 7.0 

    // Nyquist stuff ...    
    // keep the Nyquist velocity greater than any data value,
    // to avoid any folding/unfolding 
    float eff_unamb_vel = 10.0;
    float nyquist_velocity = 0.0;

    size_t nGates = NGATES_10;
    size_t clip_gate = 9;

    se_remove_ac_motion(vert_velocity, ew_velocity, ns_velocity,
                        ew_gndspd_corr, tilt, elevation,
                        data, newData, nGates, bad_flag, clip_gate,
                        eff_unamb_vel, nyquist_velocity, bnd);
    for (int i=0; i<NGATES_10; i++)
      EXPECT_EQ(newData[i], newData_expected[i]);

  }

  
  TEST(SoloRemoveSurface, remove_multifolded_ac_vel_remove_single_folded_velocity) {
 
    float data[NGATES_10] =             {-3,-3, -3, 5, 6,-4, -3,10,-12, -3};
    float newData[NGATES_10] =          { 0, 0,  0, 0, 0, 0,  0, 0, 0,   0};
    //    adjust by -1                              4  5 -5   x  9 -13
    //   unfold                                     0  1 -1   x  5  -9
    float newData_expected[NGATES_10] = {-3,-3, -3, 0, 1,-1, -3, 5, -9, -3};
    bool  bnd[NGATES_10] =              { 1, 1,  1, 1, 1, 1,  1, 1,  1,  1};

    float bad_flag = -3;

    float vert_velocity = 31; // goes with sin(elevation)
    float ew_velocity = 1;   // these three go with sin(tilt)
    float ns_velocity = 1;
    float ew_gndspd_corr = 1;
    float elevation = M_PI/2.0; // or any multiple of pi help make ac_vel = 0 
    float tilt = 0.0; // or any multiple of pi help make ac_vel = 0  
    // adjust should be -1

    // Nyquist stuff ...    
    // keep the Nyquist velocity greater than any data value,
    // to avoid any folding/unfolding 
    float eff_unamb_vel = 0.0;
    float nyquist_velocity = 2.0;

    size_t nGates = NGATES_10;
    size_t clip_gate = nGates;

    se_remove_ac_motion(vert_velocity, ew_velocity, ns_velocity,
                        ew_gndspd_corr, tilt, elevation,
                        data, newData, nGates, bad_flag, clip_gate,
                        eff_unamb_vel, nyquist_velocity, bnd);

    for (int i=0; i<NGATES_10; i++)
      EXPECT_EQ(newData[i], newData_expected[i]);

  }
*/
  /*
  TEST(SoloRemoveSurface, clipping__speckle_at_beginning__skip_speckle_at_end__no_boundary) {

    float data[NGATES_7] =             { 5, -3, -3, -3, 5, 5,-3};
    float newData[NGATES_7] =          { 0,  0,  0,  0, 0, 0, 0};
    float newData_expected[NGATES_7] = {-3, -3, -3, -3, 5, 5,-3};

    bool  bnd[NGATES_7] = {1,1,1,1,1,1,1};
    float bad_flag = -3;
    size_t a_speckle = 3;
    size_t nGates = NGATES_7;
    size_t clip_gate = 5;

    se_remove_ac_motion(data, newData, nGates, bad_flag, a_speckle, clip_gate, bnd);
    for (int i=0; i<NGATES_7; i++)
      EXPECT_EQ(newData[i], newData_expected[i]);
  }

  TEST(SoloRemoveSurface, speckle_at_boundary_edges_ignored) {
    //                                   b,  g,  g,  b, b, g, g
    float data[NGATES_7] =             {-3,  5,  5, -3,-3, 5, 5};
    float newData[NGATES_7] =          { 0,  0,  0,  0, 0, 0, 0};
    float newData_expected[NGATES_7] = {-3,  5,  5, -3,-3, 5, 5}; // no change

    bool  bnd[NGATES_7] =              { 0,  0,  1,  1, 1, 1, 0};
    float bad_flag = -3;
    size_t a_speckle = 3;
    size_t nGates = NGATES_7;
    size_t clip_gate = 5;

    se_remove_ac_motion(data, newData, nGates, bad_flag, a_speckle, clip_gate, bnd);
    for (int i=0; i<NGATES_7; i++)
      EXPECT_EQ(newData[i], newData_expected[i]);
  }
  */

}  // namespace

