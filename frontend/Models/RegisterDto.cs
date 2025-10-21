using System.ComponentModel.DataAnnotations;

namespace frontend.Models
{
    public class RegisterDto
    {
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

        [Required]
        [DataType(DataType.Password)]
        [StringLength(100, MinimumLength = 6)]
        public string Password { get; set; }

        public string FotoUrl { get; set; }
        public string HuellaRef { get; set; }
    }
}
