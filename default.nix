{ lib
, buildPythonPackage
, setuptools
, pyserial
, paho-mqtt
, redis
}:

buildPythonPackage rec {
  pname = "powermeter";
  version = "1.1.0";

  src = ./.;
  propagatedBuildInputs = [
    setuptools
    pyserial
    paho-mqtt
    redis
  ];
  doCheck = false;
  meta = with lib; {
    description = "powerraw to redis and back";
    homepage = http://localhost;
    license = licenses.mit;
    # maintainers = [ maintainers. ];
  };
}
