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

      x(1) = 3
      x(2) = 12
      x(3) = 22
      x(4) = 42
      u(1) = 9
      u(2) = 8
      u(3) = 7
      u(4) = 6

!
! test these values for n: 0, 1, 2, 3, 4, n>1000
! error values: n>1000, dimension of x,u,s,del arrays

! Hmmm, not sure how to test this, ...
! vary nx and ny ? the size of the submatrix to interpolate over?

      n = 0
      print *,''
      print *,'test n=0'
      result = inter(swdzsurf_wri,sw_or_altsurf_wri,nx_wrisurf,ny_wrisurf,nxysurfmax)
      print *,'del: ', del(1), del(2), del(3), del(4)
      print *,'s: ', s(1), s(2), s(3), s(4)

      n = 1
      print *,''
      print *,'test n=1'
      result = inter(swdzsurf_wri,sw_or_altsurf_wri,nx_wrisurf,ny_wrisurf,nxysurfmax)
      print *,'del: ', del(1), del(2), del(3), del(4)
      print *,'s: ', s(1), s(2), s(3), s(4)

      n = 2
      print *,''
      print *,'test n=2'
      result = inter(swdzsurf_wri,sw_or_altsurf_wri,nx_wrisurf,ny_wrisurf,nxysurfmax)
      print *,'del: ', del(1), del(2), del(3), del(4)
      print *,'s: ', s(1), s(2), s(3), s(4)

      n = 3
      print *,''
      print *,'test n=3'
      result = inter(swdzsurf_wri,sw_or_altsurf_wri,nx_wrisurf,ny_wrisurf,nxysurfmax)
      print *,'del: ', del(1), del(2), del(3), del(4)
      print *,'s: ', s(1), s(2), s(3), s(4)

      n = 4
      print *,''
      print *,'test n=4'
      result = inter(swdzsurf_wri,sw_or_altsurf_wri,nx_wrisurf,ny_wrisurf,nxysurfmax)
      print *,'del: ', del(1), del(2), del(3), del(4)
      print *,'s: ', s(1), s(2), s(3), s(4)

      n = 1001

      stop
      end  

