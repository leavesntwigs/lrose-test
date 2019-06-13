#include <limits.h>
#include "gtest/gtest.h"
#include "Solo/BoundaryPointMap.hh"

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

  TEST(SoloBoundary, loop_ll2xy_v3_same_origin) {

    BoundaryPointMap bpm;

    // in params ...
    PointInSpace boundary_origin;
    PointInSpace radar_origin;

    PointInSpace *p0 = &boundary_origin;
    PointInSpace *p1 = &radar_origin;

    //  bpm.dd_latlon_relative(boundary_origin, radar_origin);
    p0->latitude = 385930.99999;
    p0->longitude = 0985930.99999;
    p0->altitude = 0.0;

    p1->latitude = 385930.99999;
    p1->longitude = 0985930.99999;
    p1->altitude = 0.0;

    // out params ...
    double xx, yy, zz;


    double R_earth = bpm.dd_earthr(p1->latitude);
    bpm.loop_ll2xy_v3( &p0->latitude, &p0->longitude, &p0->altitude
                   , &xx, &yy, &zz
                   , p1->latitude, p1->longitude, p1->altitude
                   , R_earth, 1 );

    EXPECT_EQ(0.0, xx);
    EXPECT_EQ(0.0, yy);
    EXPECT_EQ(0.0, zz);
    
  }

  TEST(SoloBoundary, loop_ll2xy_v3_zero_origin) {

    BoundaryPointMap bpm;

    // in params ...
    PointInSpace boundary_origin;
    PointInSpace radar_origin;

    PointInSpace *p0 = &boundary_origin;
    PointInSpace *p1 = &radar_origin;

    //  bpm.dd_latlon_relative(boundary_origin, radar_origin);
    p0->latitude = 385930.99999;
    p0->longitude = 0985930.99999;
    p0->altitude = 0.0;

    p1->latitude = 0.0;
    p1->longitude = 0.0;
    p1->altitude = 0.0;

    // out params ...
    double xx, yy, zz;


    double R_earth = bpm.dd_earthr(p1->latitude);
    bpm.loop_ll2xy_v3( &p0->latitude, &p0->longitude, &p0->altitude
                   , &xx, &yy, &zz
                   , p1->latitude, p1->longitude, p1->altitude
                   , R_earth, 1 );

    EXPECT_EQ(0.0, xx);
    EXPECT_EQ(0.0, yy);
    EXPECT_EQ(0.0, zz);
    
  }


  /*
  TEST(SoloBoundary, latlon_relative) {

    BoundaryPointMap bpm;

    PointInSpace boundary_origin;
    PointInSpace radar_origin;

    bpm.dd_latlon_relative(boundary_origin, radar_origin);

    EXPECT_EQ(3.0, radar_origin.x);
    
  }
  */

  // NOTE: this linked list of boundaries is managed externally  

  TEST(SoloBoundary, OneBoundary_simple) {

    OneBoundary *boundary = new OneBoundary();

    boundaryList->xse_add_bnd_pt(3, 4, boundary);

    boundaryList->xse_add_bnd_pt(17, 10, boundary);

    boundaryList->xse_add_bnd_pt(30, 21, boundary);

    boundaryList->xse_add_bnd_pt(5, 23, boundary);
    EXPECT_EQ(0, 1);
  }


TEST(SoloBoundary, get_boundary_mask_same_origin) {
  
  // all data must be gridded, so x,y coordinates, plus the value

  float boundaryX[] = {};
  float boundaryY[] = {};
  float oneRayData[] = {4.0, 5.0};
  float *outData;
  float expectedValue[] = {5.0, 6.0};

  int nBoundaryPoints = 4;
  int nGates = 10;
  float gateSizeInMeters = 10;
  float rayAzimuth = 0.0;

  short *boundaryMask = new short(nBoundaryPoints);

  // boundary is a list of <list of x,y-points>
  
  radar->latitude = latitude;
  radar->longitude = longitude;
  radar->altitude = altitude;
  radar->earth_radius = dd_earthr(radar->latitude);
  radar->tilt = dd_tilt_angle(dgi);
  radar->tilt = dgi->dds->swib->fixed_angle;

  /* TODO: where I'd like to be ...
  boundaryMask = BoundaryPointMap::get_boundary_mask(boundary, 
                                                     float latitude,
                                                     float longitude,
                                                     float altitude,
                                                     float earth_radius,
                                                     float tilt,
                                                     int nGates,
                                                     float gateSize,
                                                     float azimuth);
  */

  // Where it is now ...
  OneBoundary *boundaryList = new OneBoundary();
  
  PointInSpace radar_origin;
  PointInSpace boundary_origin;
  float gateSize;
  float distanceToCellNInMeters;
  float azimuth;
  int radar_scan_mode;
  int radar_type;
  float tilt_angle;  // TODO: are tilt_angle & rotation_angle the same thing?                 
  float rotation_angle;

  radar_origin.latitude = 0.0;
  radar_origin.longitude = 0.0;
  radar_origin.altitude = 0.0;

  boundary_origin.latitude = 0.0;
  boundary_origin.longitude = 0.0;
  boundary_origin.altitude = 0.0;

 
  boundaryMask = BoundaryPointMap::get_boundary_mask(boundaryList,
                                             &radar_origin,
                                             &boundary_origin,
                                             nGates,
                                             gateSize,
                                             distanceToCellNInMeters,
                                             azimuth,
                                             radar_scan_mode,
                                             radar_type,
                                             tilt_angle,
                                             rotation_angle);



  EXPECT_EQ(0, boundaryMask[0]);
  EXPECT_EQ(0, boundaryMask[1]);
  EXPECT_EQ(0, boundaryMask[2]);
  EXPECT_EQ(0, boundaryMask[3]);
  /*
  outData = remove_ac_motion(oneRayData, boundaryMask, otherInfo);

  for (int i=0; i<nPoints; i++) {
    EXPECT_EQ(expectedValue[i], outData[i]);
  }
  */

}

}  // namespace

