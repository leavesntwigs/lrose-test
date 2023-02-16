#include <limits.h>
#include <math.h>
#include "gtest/gtest.h"
#include "Solo/SoloFunctions.hh"
#include "Radx/RadxRay.hh"
#include "Radx/RadxGeoref.hh"
#include "Radx/RadxCfactors.hh"

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
  TEST(SoloRemoveAcMotion, no_adjust__no_clipping__no_bad_flags__no_boundary) {

    float data[NGATES_4] = {3,4,5,6};
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
    // keep the Nyquist velocity greater than any data value, 
    // to avoid any folding/unfolding
    float eff_unamb_vel = 0.0; // TODO: this comes from data file?
    float nyquist_velocity = 10.0; // TODO: ???

    size_t nGates = NGATES_4;
    size_t clip_gate = nGates;
    float newData_expected[NGATES_4] = {3, 4, 5, 6};

    se_remove_ac_motion(vert_velocity, ew_velocity, ns_velocity,
			ew_gndspd_corr, tilt, elevation,
			data, newData, nGates, bad_flag, clip_gate,
			eff_unamb_vel, nyquist_velocity, bnd);
    for (int i=0; i<NGATES_4; i++)
      EXPECT_EQ(newData[i], newData_expected[i]);
    
  }

  TEST(SoloRemoveAcMotion, no_adjust__unfold__no_clipping__no_bad_flags__no_boundary) {

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
  
 
  TEST(SoloRemoveAcMotion, adjust__no_folding__clip_gate__bad_flags__no_boundary) {

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

  TEST(SoloRemoveAcMotion, adjust__folding_clip_gate__bad_flags__no_boundary) {

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
  
  TEST(SoloRemoveAcMotion, ac_vel_folded__clip_gate__no_boundary) {

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

  TEST(SoloRemoveAcMotion, ac_vel_folded__with_max_vel_instead_of_nyquist__clip_gate__no_boundary) {

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

  // *  TEST(SoloRemoveAcMotion, no_adjust__unfold__no_clipping__no_bad_flags__boundary) 
  // *   TEST(SoloRemoveAcMotion, adjust__no_folding__clip_gate__bad_flags__boundary) 
  // *     TEST(SoloRemoveAcMotion, adjust__folding_clip_gate__bad_flags__boundary) 
  // *	TEST(SoloRemoveAcMotion, ac_vel_folded__clip_gate__boundary) 
  //   *  TEST(SoloRemoveAcMotion, ac_vel_folded__with_max_vel_instead_of_nyquist__clip_gate__boundary)

  // *  TEST( ... remove_multifolded_ac_vel_remove_single_folded_velocity NOTE:  shortcoming of remove aircraft vel
  

  TEST(SoloRemoveAcMotion, no_adjust__unfold__no_clipping__no_bad_flags__boundary) {

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


  TEST(SoloRemoveAcMotion, adjust__no_folding__clip_gate__bad_flags__boundary) {
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


  
  TEST(SoloRemoveAcMotion, adjust__folding__no_clip_gate__bad_flags__boundary) {

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

  
  TEST(SoloRemoveAcMotion, ac_vel_folded__clip_gate__boundary) {

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
  
  TEST(SoloRemoveAcMotion, ac_vel_folded__with_max_vel_instead_of_nyquist__clip_gate__boundary) {
 
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

  
  TEST(SoloRemoveAcMotion, remove_multifolded_ac_vel_remove_single_folded_velocity) {
 
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

 
// I don't have any expected output for Remove_AC_Motion; no data files from Alex
// Can I make up some data? Yes. 
// 1. start with a vector of all 1's. Add aircraft motion???
//    Call remove_ac_motion, verify all 1's as a result.
// 2. Try to add some correction factors.
// 3. Use RadxRay::applyGeorefs and compare to radar_angles.  Remove_ac_motion
//    relies on the calculation of "adjust" to change to field data.  How the
//    "adjust" is calculated varies:
//    A. RadxRay::applyGeorefs
//    B. SoloII:radar_angles
//    C. A & B
//
//    Both A & B use the cfactors to calculate ra_tilt and ra_elevation which
//    AcVel uses to calculate the "adjust".
// 
//    
//

  TEST(SoloRemoveAcMotion, zero_translation_zero_rotation) {

    // fill with real data from 
    /*
    Cfac.aft
    cfrad.20181010_122951.196_to_20181010_122955.166_N42RF-TS_AIR.nc (georefApplied Y; cfactors ?)
      swp.1181010122951.N42RF-TS.196.-20.0_AIR_v3394 (CFAC block is all zero)
    expected output after running Medium QC script ...
    ** swp.MQC_1181010122951.N42RF-TS.196.-20.0_AIR_v3394 


    */
    float data[NGATES_10] =             { 1, 1,  1, 1, 1, 1,  1, 1, 1, 1};
    float newData[NGATES_10] =          { 0, 0,  0, 0, 0, 0,  0, 0, 0, 0};
    float newData_expected[NGATES_10] = { 1, 1,  1, 1, 1, 1,  1, 1, 1, 1};
    bool  bnd[NGATES_10] =              { 1, 1,  1, 1, 1, 1,  1, 1, 1, 1};
/*


    // radar_angles ...  asib means original data
    dd_radar_angles( 
  float asib_roll,
  float asib_pitch,
  float asib_heading,
  float asib_drift_angle,
  float asib_rotation_angle,
  float asib_tilt,


  float cfac_pitch_corr,
  float cfac_heading_corr,
  float cfac_drift_corr,
  float cfac_roll_corr,
  float cfac_elevation_corr,
  float cfac_azimuth_corr,
  float cfac_rot_angle_corr,
  float cfac_tilt_corr,
  int radar_type,  // from dgi->dds->radd->radar_type
  bool use_Wen_Chaus_algorithm,
    float dgi_dds_ryib_azimuth,
    float dgi_dds_ryib_elevation,
  float *ra_x,
  float *ra_y,
  float *ra_z,
  float *ra_rotation_angle,
  float *ra_tilt,
  float *ra_azimuth,  // ==> must be unique calculation for each ray???
  float *ra_elevation,
  float *ra_psi
);
*/
    float bad_flag = -3;

    float ra_elevation;
    float ra_tilt;


    // Nyquist stuff ...    
    // keep the Nyquist velocity greater than any data value,
    // to avoid any folding/unfolding 
    float eff_unamb_vel = 0.0;
    float nyquist_velocity = 2.0;

    size_t nGates = NGATES_10;
    size_t clip_gate = nGates;

    RadxRay *ray = new RadxRay();

    // RadxRay::applyGeoref(Radx::PrimaryAxis_t axis, bool force /* = true */);
    /* set these data in RadxRay because applyGeoref uses them ...
     // get georeference values

      double rollRad = _georef->getRoll() * Radx::DegToRad;
      double pitchRad = _georef->getPitch() * Radx::DegToRad;
      double headingRad = _georef->getHeading() * Radx::DegToRad;
      double tiltRad = _georef->getTilt() * Radx::DegToRad;
      double rotRad = _georef->getRotation() * Radx::DegToRad;

      // apply corrections if appropriate

      if (_cfactors) {
        rollRad += _cfactors->getRollCorr() * Radx::DegToRad;
        pitchRad += _cfactors->getPitchCorr() * Radx::DegToRad;
        headingRad += _cfactors->getHeadingCorr() * Radx::DegToRad;
        tiltRad += _cfactors->getTiltCorr() * Radx::DegToRad;
        rotRad += _cfactors->getRotationCorr() * Radx::DegToRad;
      }
    */

    RadxGeoref georef; //  = new RadxGeoref();
    /*
    georef.setLongitude();
    georef.setLatitude();
    georef.setAltitudeKmMsl(); // or setAltitudeKmAgl
    georef.setEwVelocity();
    georef.setNsVelocity();
    georef.setVertVelocity();
    georef.setHeading();
    georef.setTrack();
    georef.setRoll();
    georef.setPitch();
    georef.setDrift();
    georef.setRotation();
    georef.setTilt();
    georef.setEwWind();
    georef.setNsWind();
    georef.setVertWind();
    */

    ray->setGeoref(georef);

    RadxCfactors cfac; //  = new RadxCfactors();
    /*
    // cfactors ...
    azimuth_corr           =   0.000;
    elevation_corr         =   0.000;
    range_delay_corr       = -16.641;
    longitude_corr         =   0.000;
    latitude_corr          =   0.000;
    pressure_alt_corr      =   4.969;
    radar_alt_corr         =   0.000;
    ew_gndspd_corr         =   0.000;
    ns_gndspd_corr         =   0.000;
    vert_vel_corr          =   0.000;
    heading_corr           =   0.000;
    roll_corr              =   0.000;
    pitch_corr             =   0.009;
    drift_corr             =   0.119;
    rot_angle_corr         =  -0.016;
    tilt_corr              =   0.713;
    */
    ray->setCfactors(cfac);

    /*
    typedef enum {

      PRIMARY_AXIS_Z = 0, ///< vertical
      PRIMARY_AXIS_Y = 1, ///< longitudinal axis of platform
      PRIMARY_AXIS_X = 2, ///< lateral axis of platform
      PRIMARY_AXIS_Z_PRIME = 3, ///< inverted vertical
      PRIMARY_AXIS_Y_PRIME = 4, ///< ELDORA, HRD tail
      PRIMARY_AXIS_X_PRIME = 5  ///< translated lateral
      
    } PrimaryAxis_t;
    */

    Radx::PrimaryAxis_t axis = Radx::PRIMARY_AXIS_Y_PRIME;
    //bool force = true;
    ray->applyGeoref(axis); // , force);

    // applyGeorefs calculates phi (elevation angle), 
    // but it does NOT calculate tau (tilt) = asin (z_t)
    // we may need to modify RadxRay::applyGeorefs to calculate this, since
    // tau needs the intermediate, local value zz = z_t

    ra_elevation = ray->getElevationDeg(); // TODO: convert to radians?
    ra_tilt = 0.0; // ray->getTilt(); ore georef.getTilt()?  TODO: which coordinate systems is this tilt?

    float vert_velocity = georef.getVertVelocity() + cfac.getVertVelCorr(); // goes with sin(elevation)
    float ew_velocity = georef.getEwVelocity() + cfac.getEwVelCorr();   // these three go with sin(tilt)
    float ns_velocity = georef.getNsVelocity() + cfac.getNsVelCorr();
    float ew_gndspd_corr = 0.0; // TODO: where is this??? cfac.get??; or is it calculated?
    //float elevation = M_PI/2.0; // or any multiple of pi help make ac_vel = 0 
    //float tilt = 0.0; // or any multiple of pi help make ac_vel = 0  
    // adjust should be -1

    // NEED to handle missing values -999 (SoloII) vs -9999 (Radx)
    if (vert_velocity == Radx::missingMetaFloat) vert_velocity = 0.0;
    if (ew_velocity == Radx::missingMetaFloat) ew_velocity = 0.0;
    if (ns_velocity == Radx::missingMetaFloat) ns_velocity = 0.0;
    if (ew_gndspd_corr == Radx::missingMetaFloat) ew_gndspd_corr = 0.0;

    se_remove_ac_motion(vert_velocity, ew_velocity, ns_velocity,
                        ew_gndspd_corr, ra_tilt, ra_elevation,
                        data, newData, nGates, bad_flag, clip_gate,
                        eff_unamb_vel, nyquist_velocity, bnd);

    for (int i=0; i<NGATES_10; i++)
      EXPECT_EQ(newData[i], newData_expected[i]);
  }

  // translation means non-zero Heading, Track, Drift
  TEST(SoloRemoveAcMotion, zero_translation_nonzero_tilt_yprime) {

    // fill with real data from 
    /*
    Cfac.aft
    cfrad.20181010_122951.196_to_20181010_122955.166_N42RF-TS_AIR.nc (georefApplied Y; cfactors ?)
      swp.1181010122951.N42RF-TS.196.-20.0_AIR_v3394 (CFAC block is all zero)
    expected output after running Medium QC script ...
    ** swp.MQC_1181010122951.N42RF-TS.196.-20.0_AIR_v3394 


    */
    float data[NGATES_10] =             { 1, 1,  1, 1, 1, 1,  1, 1, 1, 1};
    float newData[NGATES_10] =          { 0, 0,  0, 0, 0, 0,  0, 0, 0, 0};
    float newData_expected[NGATES_10] = { 4, 4,  4, 4, 4, 4,  4, 4, 4, 4};
    bool  bnd[NGATES_10] =              { 1, 1,  1, 1, 1, 1,  1, 1, 1, 1};
/*


    // radar_angles ...  asib means original data
    dd_radar_angles( 
  float asib_roll,
  float asib_pitch,
  float asib_heading,
  float asib_drift_angle,
  float asib_rotation_angle,
  float asib_tilt,


  float cfac_pitch_corr,
  float cfac_heading_corr,
  float cfac_drift_corr,
  float cfac_roll_corr,
  float cfac_elevation_corr,
  float cfac_azimuth_corr,
  float cfac_rot_angle_corr,
  float cfac_tilt_corr,
  int radar_type,  // from dgi->dds->radd->radar_type
  bool use_Wen_Chaus_algorithm,
    float dgi_dds_ryib_azimuth,
    float dgi_dds_ryib_elevation,
  float *ra_x,
  float *ra_y,
  float *ra_z,
  float *ra_rotation_angle,
  float *ra_tilt,
  float *ra_azimuth,  // ==> must be unique calculation for each ray???
  float *ra_elevation,
  float *ra_psi
);
*/
    float bad_flag = -3;

    float ra_elevation;
    float ra_tilt;


    // Nyquist stuff ...    
    // keep the Nyquist velocity greater than any data value,
    // to avoid any folding/unfolding 
    float eff_unamb_vel = 0.0;
    float nyquist_velocity = 5.0;

    size_t nGates = NGATES_10;
    size_t clip_gate = nGates;

    RadxRay *ray = new RadxRay();

    // RadxRay::applyGeoref(Radx::PrimaryAxis_t axis, bool force /* = true */);
    /* set these data in RadxRay because applyGeoref uses them ...
     // get georeference values

      double rollRad = _georef->getRoll() * Radx::DegToRad;
      double pitchRad = _georef->getPitch() * Radx::DegToRad;
      double headingRad = _georef->getHeading() * Radx::DegToRad;
      double tiltRad = _georef->getTilt() * Radx::DegToRad;
      double rotRad = _georef->getRotation() * Radx::DegToRad;

      // apply corrections if appropriate

      if (_cfactors) {
        rollRad += _cfactors->getRollCorr() * Radx::DegToRad;
        pitchRad += _cfactors->getPitchCorr() * Radx::DegToRad;
        headingRad += _cfactors->getHeadingCorr() * Radx::DegToRad;
        tiltRad += _cfactors->getTiltCorr() * Radx::DegToRad;
        rotRad += _cfactors->getRotationCorr() * Radx::DegToRad;
      }
    */

    RadxGeoref georef; //  = new RadxGeoref();

    // VERY IMPORTANT to set values to zero! otherwise they are
    // set to missing values and the missing values mess up the
    // georef calculations!
    georef.setToZero();
    
    //georef.setLongitude();
    //georef.setLatitude();
    //georef.setAltitudeKmMsl(); // or setAltitudeKmAgl
    georef.setEwVelocity(0.0);
    georef.setNsVelocity(3.0);
    georef.setVertVelocity(0.0);
    georef.setHeading(0.0);
    //georef.setTrack();
    //georef.setRoll();
    georef.setPitch(0.0);
    //georef.setDrift();
    //georef.setRotation();
    georef.setTilt(90.0);
    //georef.setEwWind();
    //georef.setNsWind();
    //georef.setVertWind();    

    ray->setGeoref(georef);

    RadxCfactors cfac; //  = new RadxCfactors();
    /*
    // cfactors ...
    azimuth_corr           =   0.000;
    elevation_corr         =   0.000;
    range_delay_corr       = -16.641;
    longitude_corr         =   0.000;
    latitude_corr          =   0.000;
    pressure_alt_corr      =   4.969;
    radar_alt_corr         =   0.000;
    ew_gndspd_corr         =   0.000;
    ns_gndspd_corr         =   0.000;
    vert_vel_corr          =   0.000;
    heading_corr           =   0.000;
    roll_corr              =   0.000;
    pitch_corr             =   0.009;
    drift_corr             =   0.119;
    rot_angle_corr         =  -0.016;
    tilt_corr              =   0.713;
    */
    ray->setCfactors(cfac);
    // NOTE!!!! always pull/place the cfactors to the ray, so that
    // applyGeorefs can add them BEFORE calculating the transformations.
    /*
    typedef enum {

      PRIMARY_AXIS_Z = 0, ///< vertical
      PRIMARY_AXIS_Y = 1, ///< longitudinal axis of platform
      PRIMARY_AXIS_X = 2, ///< lateral axis of platform
      PRIMARY_AXIS_Z_PRIME = 3, ///< inverted vertical
      PRIMARY_AXIS_Y_PRIME = 4, ///< ELDORA, HRD tail
      PRIMARY_AXIS_X_PRIME = 5  ///< translated lateral
      
    } PrimaryAxis_t;
    */

    Radx::PrimaryAxis_t axis = Radx::PRIMARY_AXIS_Y_PRIME;
    //bool force = true;
    ray->applyGeoref(axis); // , force);

    // applyGeorefs calculates phi (elevation angle), 
    // but it does NOT calculate tau (tilt) = asin (z_t)
    // we may need to modify RadxRay::applyGeorefs to calculate this, since
    // tau needs the intermediate, local value zz = z_t

    ra_elevation = ray->getElevationDeg() * Radx::DegToRad; // convert to radians? Yes!
    // elevation should be zero
    double abs_err = 0.05;
    EXPECT_NEAR(ray->getElevationDeg(), 0.0, abs_err);
    ra_tilt = ray->getTiltTDeg() * Radx::DegToRad; // ray->getTilt(); or georef.getTilt()?  TODO: which coordinate systems is this tilt?
    EXPECT_NEAR(ray->getTiltTDeg(), 90.0, abs_err);
    float vert_velocity = georef.getVertVelocity() + cfac.getVertVelCorr(); // goes with sin(elevation)
    float ew_velocity = georef.getEwVelocity() + cfac.getEwVelCorr();   // these three go with sin(tilt)
    float ns_velocity = georef.getNsVelocity() + cfac.getNsVelCorr();
    float ew_gndspd_corr = 0.0; // TODO: where is this??? cfac.get??; or is it calculated?
    //float elevation = M_PI/2.0; // or any multiple of pi help make ac_vel = 0 
    //float tilt = 0.0; // or any multiple of pi help make ac_vel = 0  
    // adjust should be -1

    // NEED to handle missing values -999 (SoloII) vs -9999 (Radx)
    if (vert_velocity == Radx::missingMetaFloat) vert_velocity = 0.0;
    if (ew_velocity == Radx::missingMetaFloat) ew_velocity = 0.0;
    if (ns_velocity == Radx::missingMetaFloat) ns_velocity = 0.0;
    if (ew_gndspd_corr == Radx::missingMetaFloat) ew_gndspd_corr = 0.0;

    se_remove_ac_motion(vert_velocity, ew_velocity, ns_velocity,
                        ew_gndspd_corr, ra_tilt, ra_elevation,
                        data, newData, nGates, bad_flag, clip_gate,
                        eff_unamb_vel, nyquist_velocity, bnd);

    for (int i=0; i<NGATES_10; i++)
      EXPECT_EQ(newData[i], newData_expected[i]);
  }


  // translation means non-zero Heading, Track, Drift
  TEST(SoloRemoveAcMotion, zero_translation_nonzero_elev_nonzero_tilt_yprime) {

    float data[NGATES_10] =             { 1, 1,  1, 1, 1, 1,  1, 1, 1, 1};
    float newData[NGATES_10] =          { 0, 0,  0, 0, 0, 0,  0, 0, 0, 0};
    float newData_expected[NGATES_10] = { 5, 5,  5, 5, 5, 5,  5, 5, 5, 5};
    bool  bnd[NGATES_10] =              { 1, 1,  1, 1, 1, 1,  1, 1, 1, 1};

    float bad_flag = -3;

    float ra_elevation;
    float ra_tilt;


    // Nyquist stuff ...    
    // keep the Nyquist velocity greater than any data value,
    // to avoid any folding/unfolding 
    float eff_unamb_vel = 0.0;
    float nyquist_velocity = 5.0;

    size_t nGates = NGATES_10;
    size_t clip_gate = nGates;

    RadxRay *ray = new RadxRay();

    RadxGeoref georef; //  = new RadxGeoref();

    // VERY IMPORTANT to set values to zero! otherwise they are
    // set to missing values and the missing values mess up the
    // georef calculations!
    georef.setToZero();
    
    //georef.setLongitude();
    //georef.setLatitude();
    //georef.setAltitudeKmMsl(); // or setAltitudeKmAgl
    georef.setEwVelocity(0.0);
    georef.setNsVelocity(0.0);
    georef.setVertVelocity(4.0);
    georef.setHeading(0.0);
    //georef.setTrack();
    //georef.setRoll();
    georef.setPitch(90.0);
    //georef.setDrift();
    //georef.setRotation();
    georef.setTilt(90.0);
    //georef.setEwWind();
    //georef.setNsWind();
    //georef.setVertWind();    

    ray->setGeoref(georef);

    RadxCfactors cfac; 

    ray->setCfactors(cfac);
    // NOTE!!!! always pull/place the cfactors to the ray, so that
    // applyGeorefs can add them BEFORE calculating the transformations.

    Radx::PrimaryAxis_t axis = Radx::PRIMARY_AXIS_Y_PRIME;
    //bool force = true;
    ray->applyGeoref(axis); // , force);

    // applyGeorefs calculates phi (elevation angle), 
    // but it does NOT calculate tau (tilt) = asin (z_t)
    // we may need to modify RadxRay::applyGeorefs to calculate this, since
    // tau needs the intermediate, local value zz = z_t

    ra_elevation = ray->getElevationDeg() * Radx::DegToRad; // convert to radians? Yes!
    // elevation should be zero
    double abs_err = 0.05;
    EXPECT_NEAR(ray->getElevationDeg(), 90.0, abs_err);
    ra_tilt = ray->getTiltTDeg() * Radx::DegToRad; // ray->getTilt(); or georef.getTilt()?  TODO: which coordinate systems is this tilt?
    EXPECT_NEAR(ray->getTiltTDeg(), 0.0, abs_err);
    float vert_velocity = georef.getVertVelocity() + cfac.getVertVelCorr(); // goes with sin(elevation)
    float ew_velocity = georef.getEwVelocity() + cfac.getEwVelCorr();   // these three go with sin(tilt)
    float ns_velocity = georef.getNsVelocity() + cfac.getNsVelCorr();
    float ew_gndspd_corr = 0.0; // TODO: where is this??? cfac.get??; or is it calculated?
    //float elevation = M_PI/2.0; // or any multiple of pi help make ac_vel = 0 
    //float tilt = 0.0; // or any multiple of pi help make ac_vel = 0  
    // adjust should be -1

    // NEED to handle missing values -999 (SoloII) vs -9999 (Radx)
    if (vert_velocity == Radx::missingMetaFloat) vert_velocity = 0.0;
    if (ew_velocity == Radx::missingMetaFloat) ew_velocity = 0.0;
    if (ns_velocity == Radx::missingMetaFloat) ns_velocity = 0.0;
    if (ew_gndspd_corr == Radx::missingMetaFloat) ew_gndspd_corr = 0.0;

    se_remove_ac_motion(vert_velocity, ew_velocity, ns_velocity,
                        ew_gndspd_corr, ra_tilt, ra_elevation,
                        data, newData, nGates, bad_flag, clip_gate,
                        eff_unamb_vel, nyquist_velocity, bnd);

    for (int i=0; i<NGATES_10; i++)
      EXPECT_EQ(newData[i], newData_expected[i]);
  }

  TEST(SoloRemoveAcMotion, nonzero_translation_sensor_rotated_zero_cfacs_yprime) {

    float data[NGATES_10] =             { 1, 1,  1, 1, 1, 1,  1, 1, 1, 1};
    float newData[NGATES_10] =          { 0, 0,  0, 0, 0, 0,  0, 0, 0, 0};
    float newData_expected[NGATES_10] = { 5, 5,  5, 5, 5, 5,  5, 5, 5, 5};
    bool  bnd[NGATES_10] =              { 1, 1,  1, 1, 1, 1,  1, 1, 1, 1};
    float sin_cos_pi_over_4 = 0.7071067811865475;
    float bad_flag = -3;

    float ra_elevation;
    float ra_tilt;

    // Nyquist stuff ...    
    // keep the Nyquist velocity greater than any data value,
    // to avoid any folding/unfolding 
    float eff_unamb_vel = 0.0;
    float nyquist_velocity = 5.0;

    size_t nGates = NGATES_10;
    size_t clip_gate = nGates;

    RadxRay *ray = new RadxRay();

    RadxGeoref georef; //  = new RadxGeoref();

    // VERY IMPORTANT to set values to zero! otherwise they are
    // set to missing values and the missing values mess up the
    // georef calculations!
    georef.setToZero();
    
    //georef.setLongitude();
    //georef.setLatitude();
    //georef.setAltitudeKmMsl(); // or setAltitudeKmAgl
    georef.setEwVelocity(0.0);
    georef.setNsVelocity(0.0);
    georef.setVertVelocity(4.0);
    georef.setHeading(0.0);
    //georef.setTrack();
    georef.setRoll(-90.0);
    georef.setPitch(45.0);
    //georef.setDrift();
    georef.setRotation(90.0);  // theta_a
    georef.setTilt(0.0);
    //georef.setEwWind();
    //georef.setNsWind();
    //georef.setVertWind();    

    ray->setGeoref(georef);

    RadxCfactors cfac; 

    ray->setCfactors(cfac);
    // NOTE!!!! always pull/place the cfactors to the ray, so that
    // applyGeorefs can add them BEFORE calculating the transformations.

    Radx::PrimaryAxis_t axis = Radx::PRIMARY_AXIS_Y_PRIME;
    //bool force = true;
    ray->applyGeoref(axis); // , force);

    // applyGeorefs calculates phi (elevation angle), 
    // but it does NOT calculate tau (tilt) = asin (z_t)
    // we may need to modify RadxRay::applyGeorefs to calculate this, since
    // tau needs the intermediate, local value zz = z_t

    ra_elevation = ray->getElevationDeg() * Radx::DegToRad; // convert to radians? Yes!
    // elevation should be zero
    double abs_err = 0.05;
    EXPECT_NEAR(ray->getElevationDeg(), 45.0, abs_err);
    ra_tilt = ray->getTiltTDeg() * Radx::DegToRad; // ray->getTilt(); or georef.getTilt()?  TODO: which coordinate systems is this tilt?
    EXPECT_NEAR(ray->getTiltTDeg(), 315.0, abs_err);
    float vert_velocity = georef.getVertVelocity() + cfac.getVertVelCorr(); // goes with sin(elevation)
    float ew_velocity = georef.getEwVelocity() + cfac.getEwVelCorr();   // these three go with sin(tilt)
    float ns_velocity = georef.getNsVelocity() + cfac.getNsVelCorr();
    float ew_gndspd_corr = 0.0; // TODO: where is this??? cfac.get??; or is it calculated?
    //float elevation = M_PI/2.0; // or any multiple of pi help make ac_vel = 0 
    //float tilt = 0.0; // or any multiple of pi help make ac_vel = 0  
    // adjust should be -1

    // NEED to handle missing values -999 (SoloII) vs -9999 (Radx)
    if (vert_velocity == Radx::missingMetaFloat) vert_velocity = 0.0;
    if (ew_velocity == Radx::missingMetaFloat) ew_velocity = 0.0;
    if (ns_velocity == Radx::missingMetaFloat) ns_velocity = 0.0;
    if (ew_gndspd_corr == Radx::missingMetaFloat) ew_gndspd_corr = 0.0;

    se_remove_ac_motion(vert_velocity, ew_velocity, ns_velocity,
                        ew_gndspd_corr, ra_tilt, ra_elevation,
                        data, newData, nGates, bad_flag, clip_gate,
                        eff_unamb_vel, nyquist_velocity, bnd);

    // the ac_vel gets adjusted by mod 2*nyquist_velocity
    int adjustment = (int) (vert_velocity * sin_cos_pi_over_4) % (int) (2*nyquist_velocity);
    for (int i=0; i<NGATES_10; i++)
      newData_expected[i] = data[i] + adjustment; // sin_cos_pi_over_4;   


    for (int i=0; i<NGATES_10; i++)
      EXPECT_NEAR(newData[i], newData_expected[i], abs_err);
  }


/*
  TEST(SoloRemoveAcMotion, speckle_at_boundary_edges_ignored) {
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

