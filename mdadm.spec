# we want to install in /sbin, not /usr/sbin...
%define _exec_prefix %{nil}
%define _sbindir /sbin

Name:           mdadm
Version:        3.0
Release:        %manbo_mkrel 4
Summary:        A tool for managing Soft RAID under Linux
Group:          System/Kernel and hardware
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot
License:        GPLv2+
URL:            http://www.kernel.org/pub/linux/utils/raid/mdadm/
Source0:        http://www.kernel.org/pub/linux/utils/raid/mdadm/mdadm-%{version}.tar.bz2
Source1:        mdadm.init
Source2:        mdadm-raid-check
Source3:        mdadm-raid-check-sysconfig
Patch0:         mdadm-2.5.2-static.patch
Patch1:         mdadm-2.5.2-cflags.patch
Patch2:         mdadm-3.0-endian-FAIL.patch
Patch3:         mdadm-3.0-udev.patch
Patch4:		mdadm-3.0-detail-space.patch
Requires(post): rpm-helper
Requires(preun): rpm-helper
# udev rule used to be in udev package
Conflicts:      udev < 145-2
BuildRequires:  groff-for-man

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
%patch0 -p1 -b .static
%patch1 -p0 -b .cflags
%patch2 -p1 -b .endian
%patch3 -p1 -b .udev
%patch4 -p1 -b .detailspace
OPT_FLAGS=`/bin/echo %{optflags} | %{__sed} -e 's/-fstack-protector//'`
%{__perl} -pi -e "s/^CXFLAGS = .*/CXFLAGS = $OPT_FLAGS/" Makefile

%build
%{make} SYSCONFDIR="%{_sysconfdir}"

%install
rm -rf %{buildroot}
%{makeinstall_std} MANDIR=%{_mandir} BINDIR=%{_sbindir}
install -D -m 644 mdadm.conf-example %{buildroot}%{_sysconfdir}/mdadm.conf
install -D %{SOURCE1} %{buildroot}%{_initrddir}/mdadm
install -D %{SOURCE2} %{buildroot}%{_sysconfdir}/cron.weekly/99-raid-check
install -D -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/raid-check
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
