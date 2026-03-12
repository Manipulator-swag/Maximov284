using Microsoft.EntityFrameworkCore;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace AirportSystem
{
    public class Department
    {
        public int id { get; set; }
        public string name { get; set; }
        public string? phone { get; set; }
        public string? organization { get; set; }
    }

    public class Flight
    {

        public int id { get; set; }
        public string aircrafttype { get; set; }
        public string route { get; set; }

    }

    public class Passenger
    {
        public int id { get; set; }
        public string? fullname { get; set; }
        public string? passport { get; set; }
        public DateOnly? birthday { get; set; }
        public string gender { get; set; }
        public string position { get; set; }
        public string trippurpose { get; set; }
        public DateOnly plannedtransportdate { get; set; }
        public decimal? cargoweight { get; set; }
        public string? notes { get; set; }
        public string dp { get; set; }
        public DateOnly zayavkadate { get; set; }
        public DateOnly factdate { get; set; }
        public int zayavkanumber { get; set; }
        public int departmentid { get; set; }
        public virtual Department department { get; set; }
        public int flightid { get; set; }
        public virtual Flight flight { get; set; }

    }
    
  public class User
  {
       public int Id { get; set; }
       public string Username { get; set; }
       public string Email { get; set; }
       public string PasswordHash { get; set; }
       public string PasswordSalt { get; set; }
       public string FullName { get; set; }
       public string Role { get; set; } = "Operator";
       public bool Inactive { get; set; } = false;
       public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
       public DateTime? LastLoginAt { get; set; }
  }
}
