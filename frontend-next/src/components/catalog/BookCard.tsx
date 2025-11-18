"use client";

import { Box, VStack, Text, Image, Tag } from "@chakra-ui/react";

interface BookCardProps {
  title: string;
  author: string;
  imageUrl?: string;
  available: boolean;
}

export function BookCard({ title, author, imageUrl, available }: BookCardProps) {
  return (
    <Box
      borderWidth="1px"
      borderRadius="lg"
      overflow="hidden"
      p={4}
      minW="200px"
      maxW="200px"
      transition="all 0.2s"
      _hover={{
        shadow: "lg",
        transform: "translateY(-2px)",
        cursor: "pointer"
      }}
      bg="bg.muted"
    >
      <VStack align="stretch" gap={3}>
        <Box
          bg="gray.200"
          h="250px"
          borderRadius="md"
          display="flex"
          alignItems="center"
          justifyContent="center"
          overflow="hidden"
        >
          {imageUrl ? (
            <Image src={imageUrl} alt={title} objectFit="cover" w="full" h="full" />
          ) : (
            <Text color="gray.500" fontSize="sm">
              Sin imagen
            </Text>
          )}
        </Box>

        <VStack align="start" gap={1}>
          <Text fontWeight="bold" fontSize="sm" noOfLines={2} minH="40px">
            {title}
          </Text>
          <Text fontSize="xs" color="gray.600" noOfLines={1}>
            {author}
          </Text>
          <Tag.Root
            size="sm"
            colorPalette={available ? "green" : "red"}
            variant="solid"
          >
            {available ? "Disponible" : "No disponible"}
          </Tag.Root>
        </VStack>
      </VStack>
    </Box>
  );
}
