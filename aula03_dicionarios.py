tablespace = {
    "nome": "USERS",
    "total_gb": 500,
    "usado_gb": 350
}

percentual = tablespace["usado_gb"] / tablespace["total_gb"] * 100

print(
    f"Tablespace: {tablespace['nome']} | "
    f"Utilização: {percentual:.1f}%"
)