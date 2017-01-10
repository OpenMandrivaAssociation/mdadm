Summary:	A tool for managing Soft RAID under Linux
Name:		mdadm
Version:	4.0
Release:	1
Group:		System/Kernel and hardware
License:	GPLv2+
Url:		http://www.kernel.org/pub/linux/utils/raid/mdadm/
Source0:	http://www.kernel.org/pub/linux/utils/raid/mdadm/mdadm-%{!?git:%version}%{?git:%git}.tar.xz
%if %{?git:0}%{?!git:1}
Source1:	http://www.kernel.org/pub/linux/utils/raid/mdadm/mdadm-%{version}.tar.sign
%endif
# From Fedora
Source3:	mdadm-raid-check
Source4:	mdadm-raid-check-sysconfig
Source5:	mdadm-cron
Source6:	mdadm.rules
Source7:	mdmonitor.service
Source9:	mdadm-tmpfiles.conf
Source10:	mdadm_event.conf
Patch5:		mdadm-3.3.2-byteswap.patch

# Fedora patches
Patch197:	mdadm-3.3.2-udev.patch

# udev rule used to be in udev package
BuildRequires:	groff
BuildRequires:	binutils-devel
BuildRequires:	pkgconfig(systemd)
Requires:	libreport-filesystem

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
%make CWFLAGS=-Wall SYSCONFDIR="%{_sysconfdir}" CXFLAGS="%{optflags} -fno-strict-aliasing"

%install
make install-man install-udev DESTDIR=%{buildroot} MANDIR=%{_mandir} BINDIR=/sbin SYSTEMD_DIR=%{_unitdir} install-systemd
install -m755 mdadm -D %{buildroot}/sbin/mdadm
install -m755 mdmon -D %{buildroot}/sbin/mdmon


install -p -m644 mdadm.conf-example -D %{buildroot}%{_sysconfdir}/mdadm.conf
install -p -m755 %{SOURCE3} -D %{buildroot}%{_sbindir}/raid-check
install -p -m644 %{SOURCE4} -D %{buildroot}%{_sysconfdir}/sysconfig/raid-check
install -p -m644 %{SOURCE5} -D %{buildroot}%{_sysconfdir}/cron.d/raid-check
install -p -m755 misc/syslog-events -D %{buildroot}/sbin/mdadm-syslog-events
install -p -m644 %{SOURCE6} -D %{buildroot}%{_udevrulesdir}/65-md-incremental.rules

install -m644 %{SOURCE7} -D %{buildroot}%{_unitdir}/mdmonitor.service
install -m644 %{SOURCE9} -D %{buildroot}%{_tmpfilesdir}/%{name}.conf

install -m644 %{SOURCE10} -D %{buildroot}%{_sysconfdir}/libreport/events.d/mdadm_event.conf

%files
%doc TODO ChangeLog README.initramfs ANNOUNCE*
/sbin/mdadm
/sbin/mdadm-syslog-events
/sbin/mdmon
%{_sbindir}/raid-check
%config(noreplace) %{_sysconfdir}/cron.d/raid-check
%config(noreplace,missingok) %{_sysconfdir}/mdadm.conf
%config(noreplace) %{_sysconfdir}/sysconfig/raid-check
%{_udevrulesdir}/63-md-raid-arrays.rules
%{_udevrulesdir}/64-md-raid-assembly.rules
%{_udevrulesdir}/65-md-incremental.rules
%{_unitdir}/*.service
%{_unitdir}/*.timer
%{_systemshutdowndir}/mdadm.shutdown
%{_tmpfilesdir}/%{name}.conf
%{_sysconfdir}/libreport/events.d/*
%{_mandir}/man*/md*
