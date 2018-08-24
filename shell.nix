with import <nixpkgs> { };

(python35.withPackages (ps: [ ps.flask ps.requests ps.pyyaml ])).env
