%bcond_without	uclibc

Summary:	A tool for managing Soft RAID under Linux
Name:		mdadm
Version:	3.3.2
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
Source8:	mdmonitor-takeover.service
Source9:	mdadm-tmpfiles.conf
Source10:	mdadm_event.conf
# in situations where only ntfw and not ftw is enabled with uClibc, it's
# assumed to have neither, which this patch fixes
Patch3:		mdadm-3.2.7-uclibc-make-ntfw-work-without-ftw-enabled.patch
# add support for compiling with -fwhole-program
Patch4:		mdadm-3.3.2-whole-program.patch
Patch5:		mdadm-3.3.2-byteswap.patch

# Fedora patches
Patch197:	mdadm-3.3.2-udev.patch

# Upstream backports
Patch1000:	0001-update-add-bbl-and-no-bbl-to-the-list-of-known-updat.patch
Patch1001:	0001-Grow-Report-when-grow-needs-metadata-update.patch
Patch1002:	0001-mdmon-already-read-sysfs-files-once-after-opening.patch
Patch1003:	0001-Grow-fix-resize-of-array-component-size-to-32bits.patch
Patch1004:	0001-mdcheck-don-t-git-error-if-not-dev-md-devices-exist.patch
Patch1005:	0001-Rebuildmap-strip-local-host-name-from-device-name.patch
Patch1007:	0001-Detail-fix-handling-of-disks-array.patch
Patch1008:	0001-Incremental-don-t-be-distracted-by-partition-table-w.patch
Patch1009:	0001-imsm-support-for-OROMs-shared-by-multiple-HBAs.patch
Patch1010:	0001-imsm-support-for-second-and-combined-AHCI-controller.patch
Patch1011:	0001-imsm-add-support-for-NVMe-devices.patch
Patch1012:	0001-imsm-detail-platform-improvements.patch
Patch1013:	0001-imsm-use-efivarfs-interface-for-reading-UEFI-variabl.patch
Patch1014:	0001-Monitor-don-t-open-md-array-that-doesn-t-exist.patch
Patch1015:	0001-Grow-Fix-wrong-goto-in-set_new_data_offset.patch
Patch1016:	0001-util-remove-rounding-error-where-reporting-human-siz.patch
Patch1017:	0001-IMSM-Clear-migration-record-on-disks-more-often.patch
Patch1018:	0001-mdcheck-be-careful-when-sourcing-the-output-of-mdadm.patch
Patch1019:	0001-Monitor-fix-for-regression-with-container-devices.patch
Patch1020:	0001-Grow.c-Fix-classic-readlink-buffer-overflow.patch
Patch1021:	0001-IncrementalScan-Make-sure-st-is-valid-before-derefer.patch

# udev rule used to be in udev package
BuildRequires:	groff
BuildRequires:	binutils-devel
BuildRequires:	systemd-units
%if %{with uclibc}
BuildRequires:	uClibc-devel >= 0.9.33.2-15
%endif
Requires:	libreport-filesystem

%description
mdadm is a program that can be used to create, manage, and monitor
Linux MD (Software RAID) devices.

As such is provides similar functionality to the raidtools packages.
The particular differences to raidtools is that mdadm is a single
program, and it can perform (almost) all functions without a
configuration file (that a config file can be used to help with
some common tasks).

%package -n	uclibc-%{name}
Summary:	A tool for managing Soft RAID under Linux (uClibc build)
Group:		System/Kernel and hardware
Requires:	%{name} = %{EVRD}

%description -n	uclibc-%{name}
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
%if %{with uclibc}
mkdir .uclibc
pushd .uclibc
cp -a ../* .
popd
%endif

%build
%setup_compile_flags
%if %{with uclibc}
pushd .uclibc
make WHOLE_PROGRAM=1 CWFLAGS=-Wall CC="%{uclibc_cc}" SYSCONFDIR="%{_sysconfdir}" CXFLAGS="%{uclibc_cflags} -fno-strict-aliasing" mdadm mdmon
popd
%endif

%ifnarch aarch64
%make WHOLE_PROGRAM=1 CWFLAGS=-Wall SYSCONFDIR="%{_sysconfdir}" CXFLAGS="%{optflags} -fno-strict-aliasing"
%else
%make WHOLE_PROGRAM=0 CWFLAGS=-Wall SYSCONFDIR="%{_sysconfdir}" CXFLAGS="%{optflags} -fno-strict-aliasing"
%endif

%install
%if %{with uclibc}
install -m755 .uclibc/mdadm -D %{buildroot}%{uclibc_root}/sbin/mdadm
install -m755 .uclibc/mdmon -D %{buildroot}%{uclibc_root}/sbin/mdmon
%endif

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

%if %{with uclibc}
%files -n uclibc-%{name}
%{uclibc_root}/sbin/mdadm
%{uclibc_root}/sbin/mdmon
%endif
