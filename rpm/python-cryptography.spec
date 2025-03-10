%bcond_with tests

%define srcname cryptography

Name:           python-%{srcname}
Version:        44.0.3
Release:        0
Summary:        PyCA's cryptography library

License:        ASL 2.0 or BSD
URL:            https://github.com/sailfishos/python-cryptography
Source0:        %{name}-%{version}.tar.bz2

BuildRequires:  openssl-devel
#BuildRequires:  gcc
BuildRequires:  gnupg2

BuildRequires:  python3-cffi >= 1.12
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
#BuildRequires:  python3-setuptools-rust >= 11.4

%if %{with tests}
BuildRequires:  python3-cryptography-vectors = %{version}
BuildRequires:  python3-hypothesis >= 1.11.4
BuildRequires:  python3-iso8601
BuildRequires:  python3-pretend
BuildRequires:  python3-pytest >= 3.2.1
BuildRequires:  python3-pytz
%endif

#BuildRequires:	python3dist(packaging)
BuildRequires:	python3-pip >= 19

%description
cryptography is a package designed to expose cryptographic primitives and
recipes to Python developers.

%package -n  python3-%{srcname}
Summary:        PyCA's cryptography library
Requires:       openssl-libs

%description -n python3-%{srcname}
cryptography is a package designed to expose cryptographic primitives and
recipes to Python developers.

%prep
%autosetup -p1 -n %{name}-%{version}/upstream

%generate_buildrequires
%pyproject_buildrequires

%build
export RUSTFLAGS="%build_rustflags"
export OPENSSL_NO_VENDOR=1
export CFLAGS="${CFLAGS} -DOPENSSL_NO_ENGINE=1 "
%py3_build

%install
# Actually other *.c and *.h are appropriate
# see https://github.com/pyca/cryptography/issues/1463
find . -name .keep -print -delete
rm -rf doc

%py3_install

%check
%if %{with tests}

# enable SHA-1 signatures for RSA tests
# also see https://github.com/pyca/cryptography/pull/6931 and rhbz#2060343
export OPENSSL_ENABLE_SHA1_SIGNATURES=yes

PYTHONPATH=${PWD}/vectors:%{buildroot}%{python3_sitearch} \
    %{__python3} -m pytest \
    --ignore vendor \
    -k "not (test_buffer_protocol_alternate_modes or test_dh_parameters_supported or test_load_ecdsa_no_named_curve or test_decrypt_invalid_decrypt or test_openssl_memleak or test_load_invalid_ec_key_from_pem)"
%endif


%files -n python3-%{srcname}
%license LICENSE LICENSE.APACHE LICENSE.BSD LICENSE.dependencies
%{python3_sitearch}/%{srcname}
%{python3_sitearch}/%{srcname}-*-py*.egg-info
