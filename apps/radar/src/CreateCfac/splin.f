c
c**** FUNCTION SPLIN
c
c****************************************************************************
c
      function splin(v,x,u,s,del,q1,qn,n)
      dimension x(1000),u(1000),s(1000),del(1000)
c
      print *,'v = ', v
      print *,'x(1)= ', x(1)
      pup = v-x(1)
      print *,'v-x(1)) = ', v-x(1)
      if(v-x(1))50,10,20
  10  splin=u(1)
      print *,'option 10'
      return
  20  do k=2,n
         if(v-x(k))30,30,40
  30     k1=k-1
         ff1=s(k1)*(x(k)-v)**3.
         ff2=s(k)*(v-x(k1))**3.
         ff3=1./(6.*del(k))
         f1=(ff1+ff2)*ff3
         f2=(v-x(k1))*(u(k)/del(k)-s(k)*del(k)/6.)
         f3=(x(k)-v)*(u(k1)/del(k)-s(k1)*del(k)/6.)
         splin=f1+f2+f3
         print *,'option 20'
         return
  40     continue
      enddo
  50  splin=0.
      print *,'option 50'
c
      return
      end
