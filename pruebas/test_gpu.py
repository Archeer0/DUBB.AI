import time, torch
print("torch", torch.__version__, "| GPU visible:", torch.cuda.is_available())
def bench(dev, n=2048, reps=20):
    a = torch.randn(n, n, device=dev); b = torch.randn(n, n, device=dev)
    (a @ b).sum().item()  # calentar
    t = time.time()
    for _ in range(reps): c = a @ b
    c.sum().item()
    return time.time() - t, c
tc, cc = bench("cpu"); print(f"CPU: {tc:.2f} s")
if torch.cuda.is_available():
    print("Dispositivo:", torch.cuda.get_device_name(0))
    tg, cg = bench("cuda"); print(f"GPU: {tg:.2f} s  -> {tc/tg:.1f}x")
    a = torch.randn(512, 512); b = torch.randn(512, 512)
    err = ((a @ b) - (a.cuda() @ b.cuda()).cpu()).abs().max().item()
    print("Resultado correcto:", err < 1e-2, f"(diferencia {err:.1e})")
