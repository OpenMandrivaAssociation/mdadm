# we want to install in /sbin, not /usr/sbin...
%define _exec_prefix %{nil}
%define _sbindir /sbin
%define _usrsbindir /usr/sbin
#define git %{nil}

Name:		mdadm
Version:	3.2.1
Release:	%mkrel 1
Summary:	A tool for managing Soft RAID under Linux
Group:		System/Kernel and hardware
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
License:	GPLv2+
URL:		http://www.kernel.org/pub/linux/utils/raid/mdadm/
Source0:	http://www.kernel.org/pub/linux/utils/raid/mdadm/mdadm-%{!?git:%version}%{?git:%git}.tar.bz2
%if %{?git:0}%{?!git:1}
Source1:	http://www.kernel.org/pub/linux/utils/raid/mdadm/mdadm-%{version}.tar.bz2.sign
%endif
#From Fedora
Patch0:		mdadm-3.1.5-unused-param.patch
#From Fedora, slightly modified
Patch1:		mdadm-3.2.1-udev.patch
# fix strict aliasing with -Wstrict-alias=2
Patch2:		mdadm-3.2.1-gpt.patch
Patch3:		mdadm-3.2.1-strictalias.patch

#From Fedora, slightly modified
Source2:	mdadm.init
#From Fedora
Source3:	mdadm-raid-check
Source4:	mdadm-raid-check-sysconfig
Source5:	mdadm-cron
#From Fedora, modified because our initscripts do not use incremental assembly
# modification can be reverted only _after_ initscripts has been fixed and a
# conflict for older inistcripts is added (bluca)
Source6:	mdadm.rules
#
Requires(post):	rpm-helper
Requires(preun):	rpm-helper
# udev rule used to be in udev package
Conflicts:	udev < 145-2
%if %mdkversion < 201010
# groff-for-man should be enough but is currently broken (#56246)
BuildRequires:	groff
%else
BuildRequires:	groff-for-man >= 1.20.1-2mdv
%endif

%description
mdadm is a program that can be used to create, manage, and monitor
Linux MD (Software RAID) devices.

As such is provides similar functionality to the raidtools packages.
The particular differences to raidtools is that mdadm is a single
program, and it can perform (almost) all functions without a
configuration file (that a config file can be used to help with
some common tasks).

%prep
%setup -q %{?git:-n %name}
%patch0 -p1 -b .unused
%patch1 -p1 -b .udev
%patch2 -p1 -b .gpt
%patch3 -p1 -b .strictalias

echo "PROGRAM %{_sbindir}/mdadm-syslog-events" >> mdadm.conf-example

%build
make SYSCONFDIR="%{_sysconfdir}" CXFLAGS="%{optflags}"

%install
rm -rf %{buildroot}
%{makeinstall_std} MANDIR=%{_mandir} BINDIR=%{_sbindir}
install -Dp -m 644 mdadm.conf-example %{buildroot}%{_sysconfdir}/mdadm.conf
install -Dp %{SOURCE2} %{buildroot}%{_initrddir}/mdadm
install -Dp %{SOURCE3} %{buildroot}%{_usrsbindir}/raid-check
install -Dp -m 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/sysconfig/raid-check
install -Dp -m 644 %{SOURCE5} %{buildroot}%{_sysconfdir}/cron.d/raid-check
install -Dp misc/syslog-events %{buildroot}%{_sbindir}/mdadm-syslog-events
install -Dp -m 644 %{SOURCE6} %{buildroot}/lib/udev/rules.d/65-md-incremental.rules
mkdir -p %{buildroot}/var/run/mdadm

%clean
rm -rf %{buildroot}

%preun
%_preun_service mdadm

%post
%_post_service mdadm

%files
%defattr(644,root,root,755)
%doc TODO ChangeLog README.initramfs ANNOUNCE*
%attr(755,root,root) %{_sbindir}/mdadm
%attr(755,root,root) %{_sbindir}/mdadm-syslog-events
%attr(755,root,root) %{_sbindir}/mdmon
%attr(755,root,root) %{_usrsbindir}/raid-check
%config(noreplace) %{_sysconfdir}/cron.d/raid-check
%config(noreplace,missingok) %{_sysconfdir}/mdadm.conf
%config(noreplace) %{_sysconfdir}/sysconfig/raid-check
/lib/udev/rules.d/64-md-raid.rules
/lib/udev/rules.d/65-md-incremental.rules
%attr(755,root,root) %{_initrddir}/mdadm
%{_mandir}/man*/md*
%attr(700,root,root) %dir /var/run/mdadm
