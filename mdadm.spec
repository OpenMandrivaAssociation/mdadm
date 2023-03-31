Summary:	A tool for managing Soft RAID under Linux
Name:		mdadm
Version:	4.2
Release:	5
Group:		System/Kernel and hardware
License:	GPLv2+
Url:		http://www.kernel.org/pub/linux/utils/raid/mdadm/
Source0:	http://www.kernel.org/pub/linux/utils/raid/mdadm/mdadm-%{version}.tar.xz
Source20:	61-dracut-distro-mdraid.conf

# From Fedora
Source3:	mdadm-raid-check
Source4:	mdadm-raid-check-sysconfig
Source5:	raid-check.timer
Source6:	raid-check.service
Source7:	mdadm.rules
Source8:	mdmonitor.service
Source9:	mdadm-tmpfiles.conf
Source10:	mdadm_event.conf

# Fedora patches
Patch198:	https://src.fedoraproject.org/rpms/mdadm/raw/master/f/mdadm-4.1-no-Werror.patch

# udev rule used to be in udev package
BuildRequires:	groff
BuildRequires:	binutils-devel
BuildRequires:	pkgconfig(systemd)
BuildRequires:	pkgconfig(udev)
BuildRequires:	systemd-macros
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
%autosetup -p1

printf '%s\n' "PROGRAM %{_bindir}/mdadm-syslog-events" >> mdadm.conf-example

%build
%set_build_flags
%make_build CWFLAGS=-Wall SYSCONFDIR="%{_sysconfdir}" CXFLAGS="%{optflags} -fno-strict-aliasing"

%install
make install-man install-udev DESTDIR=%{buildroot} MANDIR=%{_mandir} BINDIR=%{_bindir} SBINDIR=%{_bindir} SYSTEMD_DIR=%{_unitdir} install-systemd
install -m755 mdadm -D %{buildroot}%{_bindir}/mdadm
install -m755 mdmon -D %{buildroot}%{_bindir}/mdmon

install -p -m644 mdadm.conf-example -D %{buildroot}%{_sysconfdir}/mdadm.conf
install -p -m755 %{SOURCE3} -D %{buildroot}%{_bindir}/raid-check
install -p -m644 %{SOURCE4} -D %{buildroot}%{_sysconfdir}/sysconfig/raid-check
install -p -m644 %{SOURCE5} -D %{buildroot}%{_unitdir}/raid-check.timer
install -p -m644 %{SOURCE6} -D %{buildroot}%{_unitdir}/raid-check.service
install -p -m755 misc/syslog-events -D %{buildroot}%{_bindir}/mdadm-syslog-events
install -p -m644 %{SOURCE7} -D %{buildroot}%{_udevrulesdir}/65-md-incremental.rules
install -m644 %{SOURCE8} -D %{buildroot}%{_unitdir}/mdmonitor.service
install -m644 %{SOURCE9} -D %{buildroot}%{_tmpfilesdir}/%{name}.conf
install -m644 %{SOURCE10} -D %{buildroot}%{_sysconfdir}/libreport/events.d/mdadm_event.conf
install -d -m 0710 %{buildroot}%{_rundir}/%{name}/

install -d %{buildroot}%{_presetdir}
cat > %{buildroot}%{_presetdir}/86-%{name}.preset << EOF
enable mdmonitor.service
enable raid-check.timer
EOF

mkdir -p %{buildroot}%{_prefix}/lib/dracut/dracut.conf.d
cp %{S:20} %{buildroot}%{_prefix}/lib/dracut/dracut.conf.d/

%post
%systemd_post mdmonitor.service raid-check.timer

%preun
%systemd_preun mdmonitor.service raid-check.timer

%postun
%systemd_postun_with_restart mdmonitor.service

%files
%doc TODO ChangeLog README.initramfs ANNOUNCE*
%{_bindir}/*
%config(noreplace,missingok) %{_sysconfdir}/mdadm.conf
%config(noreplace) %{_sysconfdir}/sysconfig/raid-check
%{_udevrulesdir}/63-md-raid-arrays.rules
%{_udevrulesdir}/64-md-raid-assembly.rules
%{_udevrulesdir}/65-md-incremental.rules
%{_udevrulesdir}/69-md-clustered-confirm-device.rules
%{_udevrulesdir}/01-md-raid-creating.rules
%{_presetdir}/86-%{name}.preset
%{_unitdir}/*.service
%{_unitdir}/*.timer
%{_systemd_util_dir}/system-shutdown/mdadm.shutdown
%{_tmpfilesdir}/%{name}.conf
%{_sysconfdir}/libreport/events.d/*
%doc %{_mandir}/man*/md*
%dir /run/%{name}/
%{_prefix}/lib/dracut/dracut.conf.d/61-dracut-distro-mdraid.conf
