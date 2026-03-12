"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { register, login } from "@/lib/api";
import { useAuth } from "@/context/AuthContext";

export default function RegisterPage() {
  const router = useRouter();
  const { refreshUser } = useAuth();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");

    try {
      await register(email, password);
      await login(email, password); // auto-login after register
      await refreshUser();
      router.push("/app");
    } catch {
      setError("Registration failed");
    }
  }

  return (
    <main className="flex min-h-screen items-center justify-center bg-neutral-950 text-neutral-100">
      <form
        onSubmit={handleSubmit}
        className="bg-neutral-900 border border-neutral-800 rounded-xl p-10 shadow-xl w-[420px] flex flex-col gap-4"
      >
        <h1 className="text-2xl font-semibold">Create Account</h1>

        <input
          type="email"
          placeholder="Email"
          className="p-2 bg-white text-black rounded"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />

        <input
          type="password"
          placeholder="Password"
          className="p-2 bg-white text-black rounded"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <button
          type="submit"
          className="bg-white text-black font-semibold py-2 rounded hover:bg-neutral-200 transition"
        >
          Register
        </button>

        {error && (
          <p className="text-red-500 text-sm">{error}</p>
        )}
      </form>
    </main>
  );
}
