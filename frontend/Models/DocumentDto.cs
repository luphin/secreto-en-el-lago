using System;
using System.ComponentModel.DataAnnotations;

namespace frontend.Models
{
    public class DocumentDto
    {
        public string Id { get; set; }

        [Required]
        [StringLength(200, MinimumLength = 1)]
        public string Titulo { get; set; }

        [Required]
        [StringLength(100, MinimumLength = 1)]
        public string Autor { get; set; }

        [Required]
        public string Editorial { get; set; }

        [Required]
        public string Edicion { get; set; }

        [Required]
        [Range(1, 2100)]
        public int AnoEdicion { get; set; }

        [Required]
        public DocumentType Tipo { get; set; }

        [Required]
        public string Categoria { get; set; }

        public string TipoMedio { get; set; }
        public int ItemsDisponibles { get; set; }
    }

    public enum DocumentType
    {
        Libro,
        Audio,
        Video
    }
}
