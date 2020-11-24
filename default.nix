let pkgs = import <nixpkgs> {};
in pkgs.mkShell {
	buildInputs = with pkgs; [
		python3Packages.black
		python3Packages.flask
		python3Packages.flask_sqlalchemy
		python3Packages.requests
		python3Packages.beautifulsoup4
		python3Packages.selenium
		python3Packages.psycopg2
		postgresql
	];
}
