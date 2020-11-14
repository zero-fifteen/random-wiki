let pkgs = import <nixpkgs> {};
in pkgs.mkShell {
	buildInputs = with pkgs.python3Packages; [
		black
		flask
		requests
		beautifulsoup4
		selenium
	];
}
