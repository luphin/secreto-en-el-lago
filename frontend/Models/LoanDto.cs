using System;
using System.ComponentModel.DataAnnotations;

namespace frontend.Models
{
    public class LoanDto
    {
        public string Id { get; set; }

        [Required]
        public string ItemId { get; set; }

        [Required]
        public string UserId { get; set; }

        [Required]
        public LoanType TipoPrestamo { get; set; }

        public DateTime FechaPrestamo { get; set; }
        public DateTime FechaDevolucionPactada { get; set; }
        public DateTime? FechaDevolucionReal { get; set; }
        public LoanStatus Estado { get; set; }
    }

    public enum LoanType
    {
        Sala,
        Domicilio
    }

    public enum LoanStatus
    {
        Activo,
        Devuelto,
        Vencido
    }
}
