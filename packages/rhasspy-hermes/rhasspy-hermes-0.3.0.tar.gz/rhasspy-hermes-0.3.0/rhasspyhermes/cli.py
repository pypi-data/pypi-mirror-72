"""Methods for command-line parsing."""
import argparse
import logging
import os
import ssl

import paho.mqtt.client as mqtt


def add_hermes_args(parser: argparse.ArgumentParser):
    """Add shared Hermes/MQTT command-line arguments."""
    parser.add_argument(
        "--host", default="localhost", help="MQTT host (default: localhost)"
    )
    parser.add_argument(
        "--port", type=int, default=1883, help="MQTT port (default: 1883)"
    )
    parser.add_argument("--username", help="MQTT username")
    parser.add_argument("--password", help="MQTT password")

    parser.add_argument("--tls", action="store_true", help="Enable MQTT TLS")
    parser.add_argument(
        "--tls-ca-certs", help="MQTT TLS Certificate Authority certificate files"
    )
    parser.add_argument("--tls-certfile", help="MQTT TLS certificate file (PEM)")
    parser.add_argument("--tls-keyfile", help="MQTT TLS key file (PEM)")
    parser.add_argument(
        "--tls-cert-reqs",
        default="CERT_REQUIRED",
        choices=["CERT_REQUIRED", "CERT_OPTIONAL", "CERT_NONE"],
        help="MQTT TLS certificate requirements (default: CERT_REQUIRED)",
    )
    parser.add_argument("--tls-version", help="MQTT TLS version (default: highest)")
    parser.add_argument("--tls-ciphers", help="MQTT TLS ciphers to use")

    parser.add_argument(
        "--site-id",
        action="append",
        help="Hermes site id(s) to listen for (default: all)",
    )
    parser.add_argument(
        "--debug", action="store_true", help="Print DEBUG messages to the console"
    )
    parser.add_argument(
        "--log-format",
        default="[%(levelname)s:%(asctime)s] %(name)s: %(message)s",
        help="Python logger format",
    )


def setup_logging(args: argparse.Namespace):
    """Set up Python logging."""
    if args.debug:
        logging.basicConfig(level=logging.DEBUG, format=args.log_format)
    else:
        logging.basicConfig(level=logging.INFO, format=args.log_format)


def connect(client: mqtt.Client, args: argparse.Namespace):
    """Connect to MQTT broker."""
    if args.username:
        client.username_pw_set(args.username, args.password)

    # TLS
    if args.tls:
        # TLS is enabled
        if args.tls_version is None:
            # Use highest TLS version
            args.tls_version = ssl.PROTOCOL_TLS

        client.tls_set(
            ca_certs=args.tls_ca_certs,
            certfile=os.path.expandvars(args.certfile),
            keyfile=os.path.expandvars(args.keyfile),
            cert_reqs=getattr(ssl, args.tls_cert_reqs),
            tls_version=args.tls_version,
            ciphers=(args.tls_ciphers or None),
        )

    client.connect(args.host, args.port)
