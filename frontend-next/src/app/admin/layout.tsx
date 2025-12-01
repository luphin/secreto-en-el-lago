"use client";

import { useEffect, useState } from "react";
import { useRouter, usePathname } from "next/navigation";
import { Box, Spinner } from "@chakra-ui/react";
import AuthService from "@/services/auth.service";

export default function AdminLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const router = useRouter();
  const pathname = usePathname();
  const [isChecking, setIsChecking] = useState(true);

  useEffect(() => {
    // No verificar en la página de login
    if (pathname === "/admin/login") {
      setIsChecking(false);
      return;
    }

    const token = AuthService.getToken();

    if (!token) {
      // No hay token, redirigir a login
      router.push("/admin/login");
    } else {
      // Hay token, permitir acceso
      setIsChecking(false);
    }
  }, [pathname, router]);

  // Mostrar spinner mientras verifica autenticación
  if (isChecking && pathname !== "/admin/login") {
    return (
      <Box
        display="flex"
        alignItems="center"
        justifyContent="center"
        minH="100vh"
        bg="bg.canvas"
      >
        <Spinner size="xl" color="purple.500" />
      </Box>
    );
  }

  return <>{children}</>;
}
