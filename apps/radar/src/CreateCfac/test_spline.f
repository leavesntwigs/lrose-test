      program test_spline

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

      !  these are filled in inter, and then passed to splin
      ! &         x(1000),
      ! &         y(1000),
      ! &         s(1000),
      ! &         d(1000)

      ! calls spline ...
      ! call spline(x,y,s,d,q1,qn,n)

      ! parameters (in/out)
      ! x (in)
      ! u (in)
      ! s (out)
      ! del (out)
      ! q1 (in)
      ! qn (in)
      ! n (in)
      ! subroutine spline(x,u,s,del,q1,qn,n)
      ! dimension x(1000),u(1000),s(1000),del(1000)
      ! dimension a(1000),v(1000)  local arrays


      x(1) = 3
      x(2) = 12
      x(3) = 22
      x(4) = 42
      u(1) = 9
      u(2) = 8
      u(3) = 7
      u(4) = 6
      ! del(1) = 0
      ! del(2) = 0
      ! del(3) = 0
      ! del(4) = 0

      q1 = 1
      qn = 1
!
! test these values for n: 0, 1, 2, 3, 4, n>1000
! error values: n>1000, dimension of x,u,s,del arrays
!
      n = 0
      print *,''
      print *,'test n=0'
      result = spline(x,u,s,del,q1,qn,n)
      print *,'del: ', del(1), del(2), del(3), del(4)
      print *,'s: ', s(1), s(2), s(3), s(4)

      n = 1
      print *,''
      print *,'test n=1'
      result = spline(x,u,s,del,q1,qn,n)
      print *,'del: ', del(1), del(2), del(3), del(4)
      print *,'s: ', s(1), s(2), s(3), s(4)

      n = 2
      print *,''
      print *,'test n=2'
      result = spline(x,u,s,del,q1,qn,n)
      print *,'del: ', del(1), del(2), del(3), del(4)
      print *,'s: ', s(1), s(2), s(3), s(4)

      n = 3
      print *,''
      print *,'test n=3'
      result = spline(x,u,s,del,q1,qn,n)
      print *,'del: ', del(1), del(2), del(3), del(4)
      print *,'s: ', s(1), s(2), s(3), s(4)

      n = 4
      print *,''
      print *,'test n=4'
      result = spline(x,u,s,del,q1,qn,n)
      print *,'del: ', del(1), del(2), del(3), del(4)
      print *,'s: ', s(1), s(2), s(3), s(4)

      n = 1001

      stop
      end  

