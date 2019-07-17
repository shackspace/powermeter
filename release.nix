with (import <nixpkgs> {});
{
  powermeter = python3.pkgs.callPackage ./default.nix {};
}
