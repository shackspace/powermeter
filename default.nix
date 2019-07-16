{ lib
, buildPythonPackage
, setuptools
, pyserial
, paho-mqtt
}:

buildPythonPackage rec {
  pname = "powermeter";
  version = "1.1.0";

  src = ./.;
  propagatedBuildInputs = [
    setuptools
    pyserial
    paho-mqtt
  ];

  meta = with lib; {
    description = "powerraw to redis and back";
    homepage = http://localhost;
    license = licenses.mit;
    # maintainers = [ maintainers. ];
  };
}
