SELECT item, COUNT(item)
FROM transacoes
GROUP BY item, COUNT(item)
ORDER BY COUNT(item) DESC
