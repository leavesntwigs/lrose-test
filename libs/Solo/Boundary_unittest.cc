#include <limits.h>
#include "gtest/gtest.h"
#include "Solo/BoundaryPointMap.hh"
#include "Solo/dd_math.h"

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
  // OneBoundary is a linked list of boundaries
  // The BoundaryPointManagement objects are a linked list of
  // boundary points, and other information, i.e. intersections, ...
  TEST(SoloBoundary, OneBoundary_simple) {
    
    OneBoundary *boundary = new OneBoundary();
    BoundaryPointMap map;

    map.xse_add_bnd_pt(3, 4, boundary);
    
    map.xse_add_bnd_pt(17, 10, boundary);
    
    map.xse_add_bnd_pt(30, 21, boundary);

    map.xse_add_bnd_pt(5, 23, boundary);
    
    EXPECT_EQ( 3.0, boundary->min_x);
    EXPECT_EQ(30.0, boundary->max_x);
    EXPECT_EQ( 4.0, boundary->min_y);
    EXPECT_EQ(23.0, boundary->max_y);

    // TODO: what are the x_ & y_mids used for?
    // TODO: what are the x_ & y_parent _right, _left used for?
    BoundaryPointManagement *x_mids = boundary->x_mids;
    EXPECT_EQ(10.0, x_mids->x_mid);
    EXPECT_EQ( 7.0, x_mids->y_mid);

    BoundaryPointManagement *y_mids = boundary->y_mids;
    EXPECT_EQ(10.0, y_mids->x_mid = 10);
    EXPECT_EQ( 7.0, y_mids->y_mid = 7);

  }

  TEST(SoloBoundary, OneBoundary_square) {
    
    OneBoundary *boundary = new OneBoundary();
    BoundaryPointMap map;

    map.xse_add_bnd_pt(2, 2, boundary);
    
    map.xse_add_bnd_pt(13, 2, boundary);
    
    map.xse_add_bnd_pt(13, 11, boundary);

    map.xse_add_bnd_pt(2, 11, boundary);
    
    EXPECT_EQ( 2.0, boundary->min_x);
    EXPECT_EQ(13.0, boundary->max_x);
    EXPECT_EQ( 2.0, boundary->min_y);
    EXPECT_EQ(11.0, boundary->max_y);
    // TODO: test the y_mid and x_mid
  }


TEST(SoloBoundary, get_boundary_mask_same_origin_where_is_zero) {
  
  // all data must be gridded, so x,y coordinates, plus the value

  float boundaryX[] = {};
  float boundaryY[] = {};
  float oneRayData[] = {4.0, 5.0};
  float *outData;
  float expectedValue[] = {5.0, 6.0};

  int nBoundaryPoints = 4;
  float gateSizeInMeters = 10;
  float rayAzimuth = 0.0;

  short *boundaryMask; //  = new short(nBoundaryPoints);

  // boundary is a list of <list of x,y-points>
  /*
  radar->latitude = latitude;
  radar->longitude = longitude;
  radar->altitude = altitude;
  radar->earth_radius = dd_earthr(radar->latitude);
  radar->tilt = dd_tilt_angle(dgi);
  radar->tilt = dgi->dds->swib->fixed_angle;
  */
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
    BoundaryPointMap map;

    map.xse_add_bnd_pt(2, 2, boundaryList);
    map.xse_add_bnd_pt(13, 2, boundaryList);
    map.xse_add_bnd_pt(13, 11, boundaryList);
    map.xse_add_bnd_pt(2, 11, boundaryList);
  
  PointInSpace radar_origin;
  PointInSpace boundary_origin;
  float gateSize = 1.5;
  int nGates = 15;
  float distanceToCellNInMeters = 3;
  float azimuth = 45.0;
  int radar_scan_mode = PPI;
  int radar_type = GROUND;
  
  // TODO: there is a current_tilt AND a boundary_radar->tilt in se_shift_bnd
  // What is the difference between these?
  // 
  float tilt_angle = 0;  // TODO: are tilt_angle & rotation_angle the same thing?                 
  float rotation_angle = azimuth;  // TODO: is this azimuth?

  radar_origin.latitude = 40.0;
  radar_origin.longitude = 40.0;
  radar_origin.altitude = 0.0;

  boundary_origin.latitude = 40.0;
  boundary_origin.longitude = 40.0;
  boundary_origin.altitude = 0.0;
  boundary_origin.tilt = 0.0;

  BoundaryPointMap bpm;
 
  
  boundaryMask = bpm.get_boundary_mask(boundaryList,
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

  

  EXPECT_EQ(1, boundaryMask[0]);
  EXPECT_EQ(1, boundaryMask[1]);
  EXPECT_EQ(1, boundaryMask[2]);
  EXPECT_EQ(1, boundaryMask[3]);
  EXPECT_EQ(1, boundaryMask[4]);
  EXPECT_EQ(1, boundaryMask[5]);
  EXPECT_EQ(1, boundaryMask[6]);
  EXPECT_EQ(1, boundaryMask[7]);
  EXPECT_EQ(1, boundaryMask[8]);
  EXPECT_EQ(0, boundaryMask[9]);
  EXPECT_EQ(0, boundaryMask[10]);
  EXPECT_EQ(0, boundaryMask[11]);
  EXPECT_EQ(0, boundaryMask[12]);
  EXPECT_EQ(0, boundaryMask[13]);
  EXPECT_EQ(0, boundaryMask[14]);
 
  /*
  outData = remove_ac_motion(oneRayData, boundaryMask, otherInfo);

  for (int i=0; i<nPoints; i++) {
    EXPECT_EQ(expectedValue[i], outData[i]);
  }
  */

}


TEST(SoloBoundary, get_boundary_mask_same_origin_zero_distance_to_gates) {
  
  // all data must be gridded, so x,y coordinates, plus the value

  float boundaryX[] = {};
  float boundaryY[] = {};
  float oneRayData[] = {4.0, 5.0};
  float *outData;
  float expectedValue[] = {5.0, 6.0};

  int nBoundaryPoints = 4;
  float gateSizeInMeters = 10;
  float rayAzimuth = 0.0;

  short *boundaryMask; //  = new short(nBoundaryPoints);

  // boundary is a list of <list of x,y-points>
  /*
  radar->latitude = latitude;
  radar->longitude = longitude;
  radar->altitude = altitude;
  radar->earth_radius = dd_earthr(radar->latitude);
  radar->tilt = dd_tilt_angle(dgi);
  radar->tilt = dgi->dds->swib->fixed_angle;
  */
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
    BoundaryPointMap map;

    map.xse_add_bnd_pt(2, 2, boundaryList);
    map.xse_add_bnd_pt(13, 2, boundaryList);
    map.xse_add_bnd_pt(13, 11, boundaryList);
    map.xse_add_bnd_pt(2, 11, boundaryList);
  
  PointInSpace radar_origin;
  PointInSpace boundary_origin;
  float gateSize = 1.5;
  int nGates = 15;
  float distanceToCellNInMeters = 0;
  float azimuth = 45.0;
  int radar_scan_mode = PPI;
  int radar_type = GROUND;
  
  // TODO: there is a current_tilt AND a boundary_radar->tilt in se_shift_bnd
  // What is the difference between these?
  // 
  float tilt_angle = 0;  // TODO: are tilt_angle & rotation_angle the same thing?                 
  float rotation_angle = azimuth;  // TODO: is this azimuth?

  radar_origin.latitude = 40.0;
  radar_origin.longitude = 40.0;
  radar_origin.altitude = 0.0;

  boundary_origin.latitude = 40.0;
  boundary_origin.longitude = 40.0;
  boundary_origin.altitude = 0.0;
  boundary_origin.tilt = 0.0;

  BoundaryPointMap bpm;
 
  
  boundaryMask = bpm.get_boundary_mask(boundaryList,
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

  boundaryList->print();
  

  EXPECT_EQ(0, boundaryMask[0]);
  EXPECT_EQ(1, boundaryMask[1]);
  EXPECT_EQ(1, boundaryMask[2]);
  EXPECT_EQ(1, boundaryMask[3]);
  EXPECT_EQ(1, boundaryMask[4]);
  EXPECT_EQ(1, boundaryMask[5]);
  EXPECT_EQ(1, boundaryMask[6]);
  EXPECT_EQ(1, boundaryMask[7]);
  EXPECT_EQ(1, boundaryMask[8]);
  EXPECT_EQ(1, boundaryMask[9]);
  EXPECT_EQ(1, boundaryMask[10]);
  EXPECT_EQ(0, boundaryMask[11]);
  EXPECT_EQ(0, boundaryMask[12]);
  EXPECT_EQ(0, boundaryMask[13]);
  EXPECT_EQ(0, boundaryMask[14]);
 
  /*
  outData = remove_ac_motion(oneRayData, boundaryMask, otherInfo);

  for (int i=0; i<nPoints; i++) {
    EXPECT_EQ(expectedValue[i], outData[i]);
  }
  */

}

}  // namespace

