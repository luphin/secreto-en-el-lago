"use client";

import { Flex, Heading, Button, Group, Input, InputGroup} from "@chakra-ui/react";
import { LuSearch, LuUser, LuBookOpen } from "react-icons/lu";
import NextLink from "next/link";

export function Header() {
  return (
    <Flex
      as="header"
      p={6}
      borderBottomWidth="1px"
      bg="bg.panel"
      gap={4}
      direction={{ base: "column", md: "row" }}
      align={{ base: "stretch", md: "center" }}
      justify="space-between"
    >
      <Heading size="lg" color="blue.600">
        Biblioteca Digital
      </Heading>

			<InputGroup flex="1" maxW={{ base: "full", md: "700px"}} startElement={<LuSearch />}>
				<Input placeholder="Buscar libros, autores, categorías..." size="md"/>
			</InputGroup>

      <Group gap={3}>
        <Button
          asChild
          variant="outline"
          colorPalette="blue"
          size="md"
        >
          <NextLink href="/login">
            <LuUser />
            Iniciar sesión
          </NextLink>
        </Button>
        <Button
          asChild
          colorPalette="blue"
          size="md"
        >
          <NextLink href="/dashboard">
            <LuBookOpen />
            Mis libros
          </NextLink>
        </Button>
      </Group>
    </Flex>
  );
}
