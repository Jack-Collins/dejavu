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

RUN dnf -y install systemd && dnf clean all && \
(cd /lib/systemd/system/sysinit.target.wants/; for i in *; do [ $i == systemd-tmpfiles-setup.service ] || rm -f $i; done); \
rm -f /lib/systemd/system/multi-user.target.wants/*;\
rm -f /etc/systemd/system/*.wants/*;\
rm -f /lib/systemd/system/local-fs.target.wants/*; \
rm -f /lib/systemd/system/sockets.target.wants/*udev*; \
rm -f /lib/systemd/system/sockets.target.wants/*initctl*; \
rm -f /lib/systemd/system/basic.target.wants/*;\
rm -f /lib/systemd/system/anaconda.target.wants/*;
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

CMD ["/usr/sbin/init"]



                                                                                 
