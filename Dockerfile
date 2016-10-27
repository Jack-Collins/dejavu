FROM fedora:23
MAINTAINER Ravel Antunes

RUN cd /usr/bin
RUN ls -a

#Add repositores for ffmpeg                                                     
RUN rpm -ivh http://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-stable.noarch.rpm \
 	&& rpm -ivh http://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-stable.noarch.rpm \
	&& rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-rpmfusion-*       

RUN dnf update -y; dnf clean all 

RUN dnf -y install numpy scipy python-matplotlib portaudio-devel ffmpeg python python-pip gcc MySQL-python pyaudio community-mysql-server community-mysql

#setup the database:

RUN systemctl start mysqld.service

RUN mysql -u root -e 'CREATE DATABASE IF NOT EXISTS dejavu; exit'

RUN pip install --upgrade pip

RUN pip install pydub
RUN pip install virtualenv
RUN virtualenv --system-site-packages env_with_system

RUN source env_with_system/bin/activate
#RUN pip install https://github.com/worldveil/dejavu/zipball/master


RUN mkdir app
ADD . /app      

CMD ["/bin/systemctl"]



                                                                                 
