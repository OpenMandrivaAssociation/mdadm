# we want to install in /sbin, not /usr/sbin...
%define _exec_prefix %{nil}
%define _sbindir /sbin
%define _usrsbindir /usr/sbin
#define git %{nil}

Name:		mdadm
Version:	3.2.5
Release:	2
Summary:	A tool for managing Soft RAID under Linux
Group:		System/Kernel and hardware
License:	GPLv2+
URL:		http://www.kernel.org/pub/linux/utils/raid/mdadm/
Source0:	http://www.kernel.org/pub/linux/utils/raid/mdadm/mdadm-%{!?git:%version}%{?git:%git}.tar.xz
%if %{?git:0}%{?!git:1}
Source1:	http://www.kernel.org/pub/linux/utils/raid/mdadm/mdadm-%{version}.tar.sign
%endif
Patch0:		mdadm-3.2.5-fix-build.diff
# From Fedora, slightly modified
Patch1:		mdadm-3.2.3-udev.patch
# don't use -Werror flag
Patch2:		mdadm-3.2.4-mdv-no_werror.patch
# From Fedora, slightly modified
Source2:	mdadm.init
# From Fedora
Source3:	mdadm-raid-check
Source4:	mdadm-raid-check-sysconfig
Source5:	mdadm-cron
# From Fedora, modified because our initscripts do not use incremental assembly
# modification can be reverted only _after_ initscripts has been fixed and a
# conflict for older inistcripts is added (bluca)
Source6:	mdadm.rules
Source7:	mdmonitor.service
Source8:	mdmonitor-takeover.service
Source9:	%{name}-tmpfiles.conf
#
Requires(post):	rpm-helper
Requires(preun):	rpm-helper
# udev rule used to be in udev package
Conflicts:	udev < 145-2
BuildRequires:	groff
BuildRequires:	binutils-devel
%if %mdvver >= 201200
BuildRequires:	systemd-units
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
%apply_patches

echo "PROGRAM %{_sbindir}/mdadm-syslog-events" >> mdadm.conf-example

%build
%setup_compile_flags
make SYSCONFDIR="%{_sysconfdir}" CXFLAGS="%{optflags}"

%install
%makeinstall_std MANDIR=%{_mandir} BINDIR=%{_sbindir}

install -Dp -m 644 mdadm.conf-example %{buildroot}%{_sysconfdir}/mdadm.conf
install -Dp %{SOURCE2} %{buildroot}%{_initrddir}/mdadm
install -Dp %{SOURCE3} %{buildroot}%{_usrsbindir}/raid-check
install -Dp -m 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/sysconfig/raid-check
install -Dp -m 644 %{SOURCE5} %{buildroot}%{_sysconfdir}/cron.d/raid-check
install -Dp misc/syslog-events %{buildroot}%{_sbindir}/mdadm-syslog-events
install -Dp -m 644 %{SOURCE6} %{buildroot}/lib/udev/rules.d/65-md-incremental.rules

%if %mdvver >= 201200
install -m 644 %{SOURCE7} %{buildroot}%{_unitdir}
install -m 644 %{SOURCE8} %{buildroot}%{_unitdir}
install -m 644 %{SOURCE9} -D %{buildroot}%{_prefix}/lib/tmpfiles.d/%{name}.conf
%endif

%post
%if %mdvver >= 201200
systemd-tmpfiles --create %{name}.conf
%endif
%_post_service mdadm

%preun
%_preun_service mdadm

%files
%doc TODO ChangeLog README.initramfs ANNOUNCE*
%{_sbindir}/mdadm
%{_sbindir}/mdadm-syslog-events
%{_sbindir}/mdmon
%{_usrsbindir}/raid-check
%config(noreplace) %{_sysconfdir}/cron.d/raid-check
%config(noreplace,missingok) %{_sysconfdir}/mdadm.conf
%config(noreplace) %{_sysconfdir}/sysconfig/raid-check
/lib/udev/rules.d/64-md-raid.rules
/lib/udev/rules.d/65-md-incremental.rules
%if %mdvver >= 201200
%{_unitdir}mdmonitor*.service
%{_prefix}/lib/tmpfiles.d/%{name}.conf
%else
%{_initrddir}/mdadm
%endif
%{_mandir}/man*/md*
