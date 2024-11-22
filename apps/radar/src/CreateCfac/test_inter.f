      program test_inter

      parameter (nvar=12,nxysurfmax=200)
 
      real x(1000),u(1000),s(1000),del(1000)
      INTEGER q1, qn, n 

    
      ! call inter(swdzsurf_wri,sw_or_altsurf_wri
      ! &                 ,nx_wrisurf,ny_wrisurf,nxysurfmax)
      !
      ! subroutine inter(sp,sz,
      !                    nx,ny,nxysurfmax)
      ! dimension sp(nxysurfmax,nxysurfmax),
      ! &         sz(nxysurfmax,nxysurfmax),
      ! end of dimensions for args

      !  these are local to inter and filled in inter, and then passed to splin
      ! &         x(1000),
      ! &         y(1000),
      ! &         s(1000),
      ! &         d(1000)

      ! subroutine inter(sp,sz,nx,ny,nxysurfmax)
      ! parameters (in/out)
      ! sp(nxysurfmax,nxysurfmax) (in)
      ! sz(nxysurfmax,nxysurfmax) (out)
      ! nx (in)
      ! ny (in)
      ! nxysurfmax (in)
      !
      ! from calling routine ...
      ! swdzsurf_wri
      ! sw_or_altsurf_wri
      ! nx_wrisurf
      ! ny_wrisurf


      dimension swdzsurf_wri(nxysurfmax,nxysurfmax)
      dimension sw_or_altsurf_wri(nxysurfmax,nxysurfmax)
      ! ?? nx_wrisurf
      ! ?? ny_wrisurf

      swdzsurf_wri(1,1) = 3
      swdzsurf_wri(1,2) = 12
      swdzsurf_wri(1,3) = 22
      swdzsurf_wri(1,4) = 42
      swdzsurf_wri(2,1) = 3
      swdzsurf_wri(2,2) = 12
      swdzsurf_wri(2,3) = 22
      swdzsurf_wri(2,4) = 42
      swdzsurf_wri(3,1) = 3
      swdzsurf_wri(3,2) = 12
      swdzsurf_wri(3,3) = 22
      swdzsurf_wri(3,4) = 42
      swdzsurf_wri(4,1) = 3
      swdzsurf_wri(4,2) = 12
      swdzsurf_wri(4,3) = 22
      swdzsurf_wri(4,4) = 42

!
! test these values for n: 0, 1, 2, 3, 4, n>1000
! error values: n>1000, dimension of x,u,s,del arrays

! Hmmm, not sure how to test this, ...
! vary nx and ny ? the size of the submatrix to interpolate over?

      ! square matrix
      nx_wrisurf = 0
      ny_wrisurf = 0
      print *,''
      print *,'test n=0'
      call inter(swdzsurf_wri,sw_or_altsurf_wri
     &                 ,nx_wrisurf,ny_wrisurf,nxysurfmax)
      print *,'sw_or_altsurf_wri: ', sw_or_altsurf_wri(1,1), sw_or_altsurf_wri(1,2), sw_or_altsurf_wri(1,3), sw_or_altsurf_wri(1,4)
      print *,'sw_or_altsurf_wri: ', sw_or_altsurf_wri(2,1), sw_or_altsurf_wri(2,2), sw_or_altsurf_wri(2,3), sw_or_altsurf_wri(2,4)
      print *,'sw_or_altsurf_wri: ', sw_or_altsurf_wri(3,1), sw_or_altsurf_wri(3,2), sw_or_altsurf_wri(3,3), sw_or_altsurf_wri(3,4)
      print *,'sw_or_altsurf_wri: ', sw_or_altsurf_wri(4,1), sw_or_altsurf_wri(4,2), sw_or_altsurf_wri(4,3), sw_or_altsurf_wri(4,4)

      nx_wrisurf = 1
      ny_wrisurf = 1
      print *,''
      print *,'test n=1'
      call inter(swdzsurf_wri,sw_or_altsurf_wri
     &                 ,nx_wrisurf,ny_wrisurf,nxysurfmax)
      print *,'sw_or_altsurf_wri: ', sw_or_altsurf_wri(1,1), sw_or_altsurf_wri(1,2), sw_or_altsurf_wri(1,3), sw_or_altsurf_wri(1,4)
      print *,'sw_or_altsurf_wri: ', sw_or_altsurf_wri(2,1), sw_or_altsurf_wri(2,2), sw_or_altsurf_wri(2,3), sw_or_altsurf_wri(2,4)
      print *,'sw_or_altsurf_wri: ', sw_or_altsurf_wri(3,1), sw_or_altsurf_wri(3,2), sw_or_altsurf_wri(3,3), sw_or_altsurf_wri(3,4)
      print *,'sw_or_altsurf_wri: ', sw_or_altsurf_wri(4,1), sw_or_altsurf_wri(4,2), sw_or_altsurf_wri(4,3), sw_or_altsurf_wri(4,4)


      nx_wrisurf = 2
      ny_wrisurf = 2
      print *,''
      print *,'test n=2'
      call inter(swdzsurf_wri,sw_or_altsurf_wri
     &                 ,nx_wrisurf,ny_wrisurf,nxysurfmax)
      print *,'sw_or_altsurf_wri: ', sw_or_altsurf_wri(1,1), sw_or_altsurf_wri(1,2), sw_or_altsurf_wri(1,3), sw_or_altsurf_wri(1,4)
      print *,'sw_or_altsurf_wri: ', sw_or_altsurf_wri(2,1), sw_or_altsurf_wri(2,2), sw_or_altsurf_wri(2,3), sw_or_altsurf_wri(2,4)
      print *,'sw_or_altsurf_wri: ', sw_or_altsurf_wri(3,1), sw_or_altsurf_wri(3,2), sw_or_altsurf_wri(3,3), sw_or_altsurf_wri(3,4)
      print *,'sw_or_altsurf_wri: ', sw_or_altsurf_wri(4,1), sw_or_altsurf_wri(4,2), sw_or_altsurf_wri(4,3), sw_or_altsurf_wri(4,4)


      nx_wrisurf = 3
      ny_wrisurf = 3
      print *,''
      print *,'test n=3'
      call inter(swdzsurf_wri,sw_or_altsurf_wri
     &                 ,nx_wrisurf,ny_wrisurf,nxysurfmax)
      print *,'sw_or_altsurf_wri: ', sw_or_altsurf_wri(1,1), sw_or_altsurf_wri(1,2), sw_or_altsurf_wri(1,3), sw_or_altsurf_wri(1,4)
      print *,'sw_or_altsurf_wri: ', sw_or_altsurf_wri(2,1), sw_or_altsurf_wri(2,2), sw_or_altsurf_wri(2,3), sw_or_altsurf_wri(2,4)
      print *,'sw_or_altsurf_wri: ', sw_or_altsurf_wri(3,1), sw_or_altsurf_wri(3,2), sw_or_altsurf_wri(3,3), sw_or_altsurf_wri(3,4)
      print *,'sw_or_altsurf_wri: ', sw_or_altsurf_wri(4,1), sw_or_altsurf_wri(4,2), sw_or_altsurf_wri(4,3), sw_or_altsurf_wri(4,4)


      nx_wrisurf = 4
      ny_wrisurf = 4
      print *,''
      print *,'test n=4'
      call inter(swdzsurf_wri,sw_or_altsurf_wri
     &                 ,nx_wrisurf,ny_wrisurf,nxysurfmax)
      print *,'sw_or_altsurf_wri: ', sw_or_altsurf_wri(1,1), sw_or_altsurf_wri(1,2), sw_or_altsurf_wri(1,3), sw_or_altsurf_wri(1,4)
      print *,'sw_or_altsurf_wri: ', sw_or_altsurf_wri(2,1), sw_or_altsurf_wri(2,2), sw_or_altsurf_wri(2,3), sw_or_altsurf_wri(2,4)
      print *,'sw_or_altsurf_wri: ', sw_or_altsurf_wri(3,1), sw_or_altsurf_wri(3,2), sw_or_altsurf_wri(3,3), sw_or_altsurf_wri(3,4)
      print *,'sw_or_altsurf_wri: ', sw_or_altsurf_wri(4,1), sw_or_altsurf_wri(4,2), sw_or_altsurf_wri(4,3), sw_or_altsurf_wri(4,4)


      ny_wrisurf = 1001

      ! rectangular  matrix

      stop
      end  

