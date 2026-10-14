/**
 * Proxy de reserva para a ViaCEP. O index.html chama a ViaCEP direto do
 * navegador; só usa esta função se a chamada direta falhar (rede/CORS).
 * Uso: /api/viacep?cep=01310100
 */
module.exports = async (req, res) => {
  const cep = String((req.query && req.query.cep) || "").replace(/\D/g, "");
  if (cep.length !== 8) return res.status(400).json({ erro: true, motivo: "CEP inválido" });
  try {
    const r = await fetch(`https://viacep.com.br/ws/${cep}/json/`, { signal: AbortSignal.timeout(10000) });
    if (!r.ok) return res.status(r.status === 400 ? 400 : 502).json({ erro: true, motivo: `HTTP ${r.status}` });
    const d = await r.json();
    res.setHeader("Cache-Control", "public, s-maxage=86400, stale-while-revalidate=604800");
    return res.status(200).json(d);
  } catch (e) {
    return res.status(502).json({ erro: true, motivo: "falha ao consultar a ViaCEP" });
  }
};
