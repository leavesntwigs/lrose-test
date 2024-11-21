c
c****************************************************************************
c
c**** SUBROUTINE SPLINE
c
c****************************************************************************
c
      subroutine spline(x,u,s,del,q1,qn,n)
      dimension x(1000),u(1000),s(1000),del(1000)
      dimension a(1000),v(1000)
c
      del(2)=x(2)-x(1)
      v(1)=6.*(((u(2)-u(1))/del(2))-q1)
      n1=n-1
      do i=2,n1
         print *,'inside loop 1'
         del(i+1)=x(i+1)-x(i)
         v(i)=((u(i-1)/del(i))-u(i)*((1./del(i))+(1./del(i+1)))
     &         +(u(i+1)/del(i+1)))*6.
      enddo
      v(n)=(qn+(u(n1)-u(n))/del(n))*6.
c
      a(1)=2.*del(2)
      a(2)=1.5*del(2)+2.*del(3)
      v(2)=v(2)-.5*v(1)
      do i=3,n1
         print *,'inside loop 2'
         c=del(i)/a(i-1)
         a(i)=2.*(del(i)+del(i+1))-c*del(i)
         v(i)=v(i)-c*v(i-1)
      enddo
      c=del(n)/a(n1)
      a(n)=2.*del(n)-c*del(n)
      v(n)=v(n)-c*v(n1)
c
      s(n)=v(n)/a(n)
      do j=1,n1
         print *,'inside loop 3'
         i=n-j
         s(i)=(v(i)-del(i+1)*s(i+1))/a(i)
      enddo
c
       return
      end
c
