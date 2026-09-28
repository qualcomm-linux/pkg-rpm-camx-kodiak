%global debug_package %{nil}
%global __os_install_post %{nil}
%global _build_id_links none

%global camx_platform    kodiak
%global camx_basedir     %{_libdir}
%global camx_compat_libdir %{_prefix}/lib
%global camx_plugin_dir  %{camx_basedir}/camx/%{camx_platform}
%global camx_hexagon_dsp_dir %{_datadir}/hexagon-dsp/qcm6490/Thundercomm/RB3gen2/dsp/cdsp

%global upstream_tag 260925
%global payload_release 1
%global payload_distro el10

%global __provides_exclude_from ^(%{camx_plugin_dir}|%{_datadir}/qcom|%{camx_hexagon_dsp_dir})/.*$
%global __requires_exclude ^lib(adsp_.*|bitml_nsp.*|bitmlenginev2|camera_hardware|camera_metadata|camera_nn_stub|camx_hardware|camx_metadata|camxcommonutils|camxexternalformatutils|camxfdengine|camxgenerated|camximageformatutils|camxifestriping|camxsensorconfig|camxtintlessalgo|chicustomization|chilog|chiofflinepostproclib|com\\.qti\\.camx\\.chiiqutils|com\\.qti\\.chinodeutils|defog|dsp_streamer.*|ipebpsstriping|ipebpsstriping170|ioteis1_26|ioteis_26|mesh_fusion26|offlinedump|shdr3|swregistrationalgo)\\.so.*$

Name:           camx-kodiak
Version:        1.0.45
Release:        1%{?dist}
Summary:        Qualcomm CamX camera driver libraries for Kodiak (QCM6490)

License:        LicenseRef-Qualcomm-Proprietary
URL:            http://support.cdmatech.com

Source0:        https://qartifactory-edge.qualcomm.com/artifactory/qsc_releases/software/chip/component/camx.qclinux.0.0/%{upstream_tag}/prebuilt_rpm/%{name}-%{version}_%{payload_release}.%{payload_distro}.aarch64.tar.gz

ExclusiveArch:  aarch64

Recommends:     qcom-adreno-cl
Recommends:     qcom-adreno-egl
Recommends:     qcom-adreno-gles2

%description
Qualcomm CamX usermode libraries for the Kodiak (QCM6490) platform.

Core camera driver components: the CamX HAL3 module, the CHI feature and node
plugin set, per-sensor tuning data, and the nativehaltest bring-up utility.
The package installs the CamX payload under %{_libdir} and provides
compatibility symlinks under /usr/lib for existing camera-service consumers.

%package devel
Summary:        Development linker symlinks for the CamX plugin libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Unversioned linker symlinks for the private CamX plugin libraries. Runtime
libraries remain in the main package as versioned .so.* files.

%package -n libcamx-kodiak1
Summary:        Qualcomm CamX libraries for camera service
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n libcamx-kodiak1
Runtime CamX libraries used by the QMMF camera service on the Kodiak
(QCM6490) platform.

This package provides the CamX hardware and metadata libraries required by
the camera service. The real libraries are installed under %{_libdir};
compatibility symlinks are provided under /usr/lib.

%package -n libcamx-kodiak-devel
Summary:        Development files for the CamX camera service libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       libcamx-kodiak1%{?_isa} = %{version}-%{release}

%description -n libcamx-kodiak-devel
Unversioned .so linker symlinks for the CamX camera service (QMMF) libraries
on the Kodiak platform.

Symlinks only -- no headers. The consumer-facing CamX headers are packaged
separately as libcamx-dev from the target-agnostic headers tarball.

%prep
%setup -q -n %{name}-%{version}

%build

%install
cp -a usr %{buildroot}/

# Keep real CamX files under %{_libdir} and provide /usr/lib compatibility links.
install -d %{buildroot}%{camx_compat_libdir}
if [ ! -e %{buildroot}%{camx_compat_libdir}/camx ] && [ ! -L %{buildroot}%{camx_compat_libdir}/camx ]; then
    ln -s %{camx_basedir}/camx %{buildroot}%{camx_compat_libdir}/camx
fi

for _lib in %{buildroot}%{camx_basedir}/lib*_kodiak.so*; do
    [ -e "${_lib}" ] || [ -L "${_lib}" ] || continue
    _name=${_lib##*/}
    if [ ! -e %{buildroot}%{camx_compat_libdir}/${_name} ] && [ ! -L %{buildroot}%{camx_compat_libdir}/${_name} ]; then
        ln -s %{camx_basedir}/${_name} %{buildroot}%{camx_compat_libdir}/${_name}
    fi
done

rm -rf %{buildroot}%{_includedir}/camx-v1
rm -rf %{buildroot}%{_includedir}/camx
rm -rf %{buildroot}%{_includedir}/autogen
rm -rf %{buildroot}%{_defaultlicensedir}/libcamx-dev
rm -rf %{buildroot}%{_defaultlicensedir}/camx-kodiak-devel
rm -rf %{buildroot}%{_docdir}/libcamx-dev
rm -rf %{buildroot}%{_docdir}/camx-kodiak-devel

%files
%dir %{_defaultlicensedir}/%{name}
%license %{_defaultlicensedir}/%{name}/LICENSE.qcom-2
%doc %{_docdir}/%{name}/NOTICE

%{camx_basedir}/camx
%{camx_compat_libdir}/camx

# Keep private linker symlinks out of the runtime package. Otherwise RPM scans
# them and creates dependencies on libraries resolved internally by CamX.
%exclude %{camx_plugin_dir}/*.so
%exclude %{camx_plugin_dir}/hw/*.so
%exclude %{camx_plugin_dir}/camera/*.so
%exclude %{camx_plugin_dir}/camera/components/*.so

%dir %{_libexecdir}/%{name}
%{_libexecdir}/%{name}/nativehaltest

%dir %{_datadir}/camx
%{_datadir}/camx/*.bin

%{camx_hexagon_dsp_dir}/*.so

%files -n libcamx-kodiak1
%dir %{_defaultlicensedir}/libcamx-kodiak1
%license %{_defaultlicensedir}/libcamx-kodiak1/LICENSE.qcom-2
%doc %{_docdir}/libcamx-kodiak1/NOTICE
%{camx_basedir}/lib*_kodiak.so.*
%{camx_compat_libdir}/lib*_kodiak.so.*

%files -n libcamx-kodiak-devel
%dir %{_defaultlicensedir}/libcamx-kodiak-devel
%license %{_defaultlicensedir}/libcamx-kodiak-devel/LICENSE.qcom-2
%doc %{_docdir}/libcamx-kodiak-devel/NOTICE
%{camx_basedir}/lib*_kodiak.so
%{camx_compat_libdir}/lib*_kodiak.so

%files devel
%{camx_plugin_dir}/*.so
%{camx_plugin_dir}/hw/*.so
%{camx_plugin_dir}/camera/*.so
%{camx_plugin_dir}/camera/components/*.so

%changelog
* Mon Sep 28 2026 Qualcomm Camera Team <camx.deb.maintainers@qti.qualcomm.com> - 1.0.45-1
- Initial RPM release for the prebuilt Kodiak CamX payload.
- Move private CamX linker symlinks to a devel subpackage.
