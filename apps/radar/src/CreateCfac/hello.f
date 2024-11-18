      program hello
      ! This is a comment line; it is ignored by the compiler

      real*4   a(2,2)
      real*4   b(2)
      real*4   x(2)
      INTEGER n
      INTEGER ierr

      a(1,1) = 1.0
      a(1,2) = 2.0
      a(2,1) = 3.0
      a(2,2) = 5.0
      b(1) = 1.0
      b(2) = 2.0 
      n = 2
      call chol_inv(a,x,b,n,ierr)
      print *,'x: ',x(1),x(2)
      stop
      end  

