      program test_splin
      ! This is a comment line; it is ignored by the compiler


      real x(1000),u(1000),s(1000),del(1000)
      real v
      INTEGER q1, qn, n 

    
      ! 	    call inter(swdzsurf_wri,sw_or_altsurf_wri
      ! &                 ,nx_wrisurf,ny_wrisurf,nxysurfmax)
      !
      !       subroutine inter(sp,sz,
      !                    nx,ny,nxysurfmax)
      ! dimension sp(nxysurfmax,nxysurfmax),
      ! &         sz(nxysurfmax,nxysurfmax),
      ! end of dimensions for args

      !  these are filled in inter, and then passed to splin
      ! &         x(1000),
      ! &         y(1000),
      ! &         s(1000),
      ! &         d(1000)

      ! calls splin ...
      ! val=splin(yj,x,y,s,d,q1,qn,n) 

      ! function splin(v,x,u,s,del,q1,qn,n)
      ! dimension x(1000),u(1000),s(1000),del(1000)
      !    v, q1, qn, n are all single values

      x(1) = 3
      x(2) = 12
      x(3) = 22
      x(4) = 42
      u(1) = 9
      u(2) = 8
      u(3) = 7
      u(4) = 6
      del(1) = 1
      del(2) = 1
      del(3) = 1
      del(4) = 1

      n = 4
      ! test: v-x(1) < 0 
      v = 1 
      result = splin(v,x,u,s,del,q1,qn,n)
      print *,'result: ', result
      print *,'x: ', x(1), x(2), x(3) 
      print *,'u: ', u(1), u(2), u(3) 
      ! test: v-x(1) == 0 
      v = x(1) 
      result = splin(v,x,u,s,del,q1,qn,n)
      print *,'result: ', result
      print *,'x: ', x(1), x(2), x(3) 
      print *,'u: ', u(1), u(2), u(3) 
      ! test: v-x(1) > 0 && v-x(2:n) > 0
      v = 50
      result = splin(v,x,u,s,del,q1,qn,n)
      print *,'result: ', result
      print *,'x: ', x(1), x(2), x(3) 
      print *,'u: ', u(1), u(2), u(3) 
      ! test: v-x(1) > 0  && v-x(2:n) <= 0
      v = 5 
      result = splin(v,x,u,s,del,q1,qn,n)
      print *,'result: ', result
      print *,'x: ', x(1), x(2), x(3) 
      print *,'u: ', u(1), u(2), u(3) 


      n = 10

      stop
      end  

