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
Requires(preun):rpm-helper
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
%setup -q %{?git:-n %{name}}
%apply_patches

echo "PROGRAM /sbin/mdadm-syslog-events" >> mdadm.conf-example

%build
%setup_compile_flags
make SYSCONFDIR="%{_sysconfdir}" CXFLAGS="%{optflags}"

%install
%makeinstall_std MANDIR=%{_mandir} BINDIR=/sbin

install -p -m644 mdadm.conf-example -D %{buildroot}%{_sysconfdir}/mdadm.conf
install -p -m755 %{SOURCE2} -D %{buildroot}%{_initrddir}/mdadm
install -p -m755 %{SOURCE3} -D %{buildroot}%{_sbindir}/raid-check
install -p -m644 %{SOURCE4} -D %{buildroot}%{_sysconfdir}/sysconfig/raid-check
install -p -m644 %{SOURCE5} -D %{buildroot}%{_sysconfdir}/cron.d/raid-check
install -p -m755 misc/syslog-events -D %{buildroot}/sbin/mdadm-syslog-events
install -p -m644 %{SOURCE6} -D %{buildroot}/lib/udev/rules.d/65-md-incremental.rules

%if %{mdvver} >= 201200
install -m644 %{SOURCE7} -D %{buildroot}%{_unitdir}/mdmonitor.service
install -m644 %{SOURCE8} -D %{buildroot}%{_unitdir}/mdmonitor-takeover.service
ln -s mdmonitor.service %{buildroot}%{_unitdir}/mdadm.service
install -m644 %{SOURCE9} -D %{buildroot}%{_prefix}/lib/tmpfiles.d/%{name}.conf
rm -rf %{buildroot}%{_initrddir}/mdadm
%endif

%post
%if %{mdvver} >= 201200
systemd-tmpfiles --create %{name}.conf
%endif
%_post_service mdadm

%preun
%_preun_service mdadm

%files
%doc TODO ChangeLog README.initramfs ANNOUNCE*
/sbin/mdadm
/sbin/mdadm-syslog-events
/sbin/mdmon
%{_sbindir}/raid-check
%config(noreplace) %{_sysconfdir}/cron.d/raid-check
%config(noreplace,missingok) %{_sysconfdir}/mdadm.conf
%config(noreplace) %{_sysconfdir}/sysconfig/raid-check
/lib/udev/rules.d/64-md-raid.rules
/lib/udev/rules.d/65-md-incremental.rules
%if %{mdvver} >= 201200
%{_unitdir}/*.service
%{_prefix}/lib/tmpfiles.d/%{name}.conf
%else
%{_initrddir}/mdadm
%endif
%{_mandir}/man*/md*
