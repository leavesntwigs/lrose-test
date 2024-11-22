c
c****************************************************************************
c
c**** INTERPOLATION TO FILL THE HOLES IN THE RADAR-DERIVED SURFACE MAP
c
c****************************************************************************
c
      subroutine inter(sp,sz,nx,ny,nxysurfmax)
      dimension sp(nxysurfmax,nxysurfmax),sz(nxysurfmax,nxysurfmax)
     &         ,x(1000),y(1000),s(1000),d(1000)
      nsaut=5
      nmin=5
      spmin=1.
      nin=0
      nintx=0
      ninty=0
      nout=0
c
      do j=1,ny
         do i=1,nx
            if(sp(i,j).gt.spmin)then
              sz(i,j)=sz(i,j)/sp(i,j)
              nin=nin+1
	    else
	      sz(i,j)=-999.
            endif
         enddo
      enddo
c
      print *,'     -> ALONG X'
      do j=1,ny
         imax=1
  1      imin=imax
	 iant=0
	 n=0
	 do i=imin,nx
	    imax=i
	    if(sz(i,j).gt.-900.)then
	      if(iant.ne.0.and.(i-iant).gt.nsaut+1)go to 2
	      iant=i
	      n=n+1
	      x(n)=float(i)
	      y(n)=sz(i,j)
            endif
         enddo
  2      if(n.ge.nmin)then
	   q1=(y(2)-y(1))/(x(2)-x(1))
	   qn=(y(n)-y(n-1))/(x(n)-x(n-1))
	   call spline(x,y,s,d,q1,qn,n)
	   do i=imin,imax
              if(sz(i,j).lt.-900.)then
	        xi=float(i)
	        val=splin(xi,x,y,s,d,q1,qn,n)
                if(val.gt.0.)then
                  sz(i,j)=val
                  nintx=nintx+1
                endif
              endif
           enddo
         endif
	 if(imax.le.(nx-nsaut+1))go to 1
      enddo
c
      print *,'     -> ALONG Y'
      do i=1,nx
         jmax=1
  3      jmin=jmax
         jant=0
 	 n=0
	 do j=jmin,ny
	    jmax=j
	    if(sz(i,j).gt.-900.)then
	      if(jant.ne.0.and.(j-jant).gt.nsaut+1)go to 4
	      jant=j
	      n=n+1
	      x(n)=float(j)
	      y(n)=sz(i,j)
            endif
         enddo
  4      if(n.ge.nmin)then
	   q1=(y(2)-y(1))/(x(2)-x(1))
	   qn=(y(n)-y(n-1))/(x(n)-x(n-1))
	   call spline(x,y,s,d,q1,qn,n)
	   do j=jmin,jmax
              if(sz(i,j).lt.-900.)then
	        yj=float(j)
	        val=splin(yj,x,y,s,d,q1,qn,n)
                if(val.gt.0.)then
                  sz(i,j)=val
                  ninty=ninty+1
                  nput=nout+1
                endif
              else
                nout=nout+1
              endif
           enddo
         endif
	 if(jmax.le.(ny-nmin+1))go to 3
      enddo
c
      print *,'     -> N_in,int_X,int_Y,out :',nin,nintx,ninty,nout
c
      return
      end
c
