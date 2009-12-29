# we want to install in /sbin, not /usr/sbin...
%define _exec_prefix %{nil}
%define _sbindir /sbin

Name:           mdadm
# NOTE! DO NOT UPDATE TO 3.1.x SERIES YET!
# We dont consider it safe yet! bluca / tmb
Version:        3.0.3
Release:        %manbo_mkrel 2
Summary:        A tool for managing Soft RAID under Linux
Group:          System/Kernel and hardware
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot
License:        GPLv2+
URL:            http://www.kernel.org/pub/linux/utils/raid/mdadm/
Source0:        http://www.kernel.org/pub/linux/utils/raid/mdadm/mdadm-%{version}.tar.bz2
Source1:        http://www.kernel.org/pub/linux/utils/raid/mdadm/mdadm-%{version}.tar.bz2.sign
Patch0:         mdadm-2.5.2-cflags.patch
Patch1:         mdadm-3.0-udev.patch
#From Fedora
Source2:        mdadm.init
Source3:        mdadm-raid-check
Source4:        mdadm-raid-check-sysconfig
Patch2:         mdadm-3.0-metadata.patch
Patch3:         mdadm-3.0-uuid.patch
Patch4:         mdadm-3.0-mdmon-dev-.mdadm.patch
Patch5:         mdadm-3.0.3-intel-serial.patch
# from Dan Williams git
patch1000:      mdadm-3.0.3-imsm-git.patch
Requires(post): rpm-helper
Requires(preun): rpm-helper
# udev rule used to be in udev package
Conflicts:      udev < 145-2
# groff-for-man should be enough but is currently broken (#56246)
BuildRequires:  groff

%description
mdadm is a program that can be used to create, manage, and monitor
Linux MD (Software RAID) devices.

As such is provides similar functionality to the raidtools packages.
The particular differences to raidtools is that mdadm is a single
program, and it can perform (almost) all functions without a
configuration file (that a config file can be used to help with
some common tasks).

%prep
%setup -q
%patch1000 -p1 -b .imsm
%patch0 -p0 -b .cflags
%patch1 -p1 -b .udev
%patch2 -p1 -b .metadata
%patch3 -p1 -b .uuid
%patch4 -p1 -b .mdmon
%patch5 -p1 -b .serial
OPT_FLAGS=`/bin/echo %{optflags} | %{__sed} -e 's/-fstack-protector//'`
%{__perl} -pi -e "s/^CXFLAGS = .*/CXFLAGS = $OPT_FLAGS/" Makefile

%build
%{make} SYSCONFDIR="%{_sysconfdir}"

%install
rm -rf %{buildroot}
%{makeinstall_std} MANDIR=%{_mandir} BINDIR=%{_sbindir}
install -D -m 644 mdadm.conf-example %{buildroot}%{_sysconfdir}/mdadm.conf
install -D %{SOURCE2} %{buildroot}%{_initrddir}/mdadm
install -D %{SOURCE3} %{buildroot}%{_sysconfdir}/cron.weekly/99-raid-check
install -D -m 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/sysconfig/raid-check
mkdir -p %{buildroot}/var/run/mdadm

%clean
rm -rf %{buildroot}

%preun
%_preun_service mdadm

%post
%_post_service mdadm

%files
%defattr(644,root,root,755)
%doc TODO ChangeLog mdadm.conf-example README.initramfs ANNOUNCE* misc/*
%attr(755,root,root) %{_sbindir}/mdadm
%attr(755,root,root) %{_sbindir}/mdmon
%attr(755,root,root) %{_sysconfdir}/cron.weekly/99-raid-check
%config(noreplace,missingok) %{_sysconfdir}/mdadm.conf
%config(noreplace) %{_sysconfdir}/sysconfig/raid-check
/lib/udev/rules.d/64-md-raid.rules
%attr(755,root,root) %{_initrddir}/mdadm
%{_mandir}/man*/md*
%attr(700,root,root) %dir /var/run/mdadm
