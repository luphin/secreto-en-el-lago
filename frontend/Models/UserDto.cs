using System;
using System.ComponentModel.DataAnnotations;

namespace frontend.Models
{
    public class UserDto
    {
        public string Id { get; set; }

        [Required]
        [StringLength(12, MinimumLength = 9, ErrorMessage = "RUT debe tener entre 9 y 12 caracteres")]
        public string Rut { get; set; }

        [Required]
        [StringLength(50, MinimumLength = 1)]
        public string Nombres { get; set; }

        [Required]
        [StringLength(50, MinimumLength = 1)]
        public string Apellidos { get; set; }

        [Required]
        public string Direccion { get; set; }

        [Required]
        [Phone]
        public string Telefono { get; set; }

        [Required]
        [EmailAddress]
        public string Email { get; set; }

        public UserRole Rol { get; set; }
        public bool Activo { get; set; }
        public DateTime FechaCreacion { get; set; }
        public string FotoUrl { get; set; }
        public string HuellaRef { get; set; }
        public DateTime? SancionHasta { get; set; }
    }

    public enum UserRole
    {
        Lector,
        Bibliotecario,
        Administrativo
    }
}
