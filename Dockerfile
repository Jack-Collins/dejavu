FROM fedora:24
MAINTAINER Ravel Antunes

#Add repositores for ffmpeg                                                     
RUN rpm -ivh http://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-stable.noarch.rpm \
 	&& rpm -ivh http://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-stable.noarch.rpm \
	&& rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-rpmfusion-*       

RUN dnf update -y; dnf clean all 

RUN dnf -y install numpy scipy python-matplotlib portaudio-devel ffmpeg python python-pip gcc MySQL-python pyaudio community-mysql-server community-mysql

RUN pip install --upgrade pip

RUN pip install pydub
RUN pip install porc

RUN pip install virtualenv
RUN virtualenv --system-site-packages env_with_system

RUN source env_with_system/bin/activate
#RUN pip install https://github.com/worldveil/dejavu/zipball/master


RUN mkdir app
ADD . /app      




                                                                                 
